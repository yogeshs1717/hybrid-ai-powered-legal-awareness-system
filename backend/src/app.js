"use strict";

const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const morgan = require("morgan");
const { v4: uuidv4 } = require("uuid");

const config = require("./config");
const { validateAnalyzeInput } = require("./validate");
const { analyzeRateLimiter } = require("./rateLimiter");
const { buildLogRecord, logAnalysis } = require("./logger");
const { createMlClient } = require("./mlClient");
const { translateText, translateArray, detectScript } = require("./translator");

// The five approved Phase 1 domains (CLAUDE.md Section 3.1). Display metadata
// only — the gateway holds no legal logic.
const DOMAINS = [
  { id: "cyber_fraud", display_name: "Cyber Fraud" },
  { id: "consumer_issues", display_name: "Consumer Issues" },
  { id: "traffic_enforcement", display_name: "Traffic Enforcement" },
  { id: "workplace_wage", display_name: "Workplace / Wage" },
  { id: "contractual_disputes", display_name: "Contractual Disputes" },
];

// App factory. `mlClient` is injectable for testing; defaults to the real one.
function createApp({ mlClient = createMlClient() } = {}) {
  const app = express();

  app.use(helmet());
  app.use(cors());
  app.use(express.json({ limit: "16kb" }));
  app.use(morgan("tiny")); // access log: method/url/status/time — no body, no PII

  // Attach a UUID request_id to every request (CLAUDE.md Section 4.4).
  app.use((req, _res, next) => {
    req.requestId = uuidv4();
    next();
  });

  // Malformed JSON body -> 400 (input validation, not a server error).
  app.use((err, req, res, next) => {
    if (err && err.type === "entity.parse.failed") {
      return res.status(400).json({
        success: false,
        error: "invalid_input",
        detail: "Request body must be valid JSON.",
      });
    }
    return next(err);
  });

  app.get("/api/health", async (_req, res) => {
    let ml = { reachable: false };
    try {
      const r = await mlClient.health();
      ml = { reachable: r.status === 200, ...(r.data || {}) };
    } catch (_e) {
      ml = { reachable: false };
    }
    res.json({ success: true, gateway: "ok", ml_service: ml });
  });

  app.get("/api/domains", (_req, res) => {
    res.json({ success: true, domains: DOMAINS });
  });

  // Translation endpoint for dynamic text translation (English, Hindi, Kannada)
  app.post("/api/translate", async (req, res) => {
    const target = req.body?.target || req.body?.targetLang || req.body?.target_lang || "en";
    const source = req.body?.source || req.body?.sourceLang || req.body?.source_lang || "auto";
    const { text, texts } = req.body || {};
    if (!text && !Array.isArray(texts)) {
      return res.status(400).json({
        success: false,
        error: "invalid_input",
        detail: "Field 'text' (string) or 'texts' (array of strings) is required.",
      });
    }

    if (text) {
      const translated = await translateText(String(text), target, source);
      return res.json({ success: true, translated, target, source });
    }

    const translated = await translateArray(texts, target, source);
    return res.json({ success: true, translated, target, source });
  });

  app.post("/api/analyze", analyzeRateLimiter, validateAnalyzeInput, async (req, res) => {
    const requestId = req.requestId;
    const scenario = req.validatedScenario;
    const detectedScript = detectScript(scenario);

    // If citizen typed in Hindi or Kannada, translate to English for the ML pipeline
    let analysisScenario = scenario;
    let inputLanguage = detectedScript;
    if (detectedScript !== "en") {
      try {
        const engText = await translateText(scenario, "en", detectedScript);
        if (engText && engText.trim().length >= 10) {
          analysisScenario = engText.trim();
        }
      } catch (_e) {
        // Fall back to original scenario if translation fails
      }
    }

    try {
      const { status, data } = await mlClient.analyze({ scenario: analysisScenario, requestId });

      // Anonymized logging — never logs scenario text (CLAUDE.md Section 9).
      logAnalysis(
        buildLogRecord({
          requestId,
          scenario,
          statusCode: status,
          mlBody: data,
          language: inputLanguage,
        })
      );

      // Return the ML response body UNCHANGED (contract preserved, CLAUDE.md Section 8.1).
      // Pass the ML status through.
      if (inputLanguage && inputLanguage !== "en") {
        res.setHeader("X-Detected-Language", inputLanguage);
      }
      return res.status(status).json(data);
    } catch (err) {
      // ML service unreachable / timed out -> 503; never fabricate a legal answer.
      logAnalysis(
        buildLogRecord({ requestId, scenario, statusCode: 503, mlBody: null, language: inputLanguage })
      );
      return res.status(503).json({
        success: false,
        request_id: requestId,
        error: "ml_service_unavailable",
        detail: "The analysis service is temporarily unavailable. Please try again.",
      });
    }
  });

  app.use((_req, res) => {
    res.status(404).json({ success: false, error: "not_found" });
  });

  return app;
}

module.exports = { createApp, DOMAINS };

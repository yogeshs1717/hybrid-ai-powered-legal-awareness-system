"use strict";

const config = require("./config");

// Input validation middleware for POST /api/analyze.
// Validation failures are client errors -> HTTP 400 (CLAUDE.md Section 8.2).
// This is distinct from low ML confidence, which the ML service returns as 200.

function validateAnalyzeInput(req, res, next) {
  const body = req.body || {};
  const { scenario } = body;

  if (typeof scenario !== "string") {
    return res.status(400).json({
      success: false,
      error: "invalid_input",
      detail: "Field 'scenario' is required and must be a string.",
    });
  }

  const trimmed = scenario.trim();
  if (trimmed.length < config.scenarioMinLength) {
    return res.status(400).json({
      success: false,
      error: "invalid_input",
      detail: `Scenario must be at least ${config.scenarioMinLength} characters.`,
    });
  }
  if (trimmed.length > config.scenarioMaxLength) {
    return res.status(400).json({
      success: false,
      error: "invalid_input",
      detail: `Scenario must be at most ${config.scenarioMaxLength} characters.`,
    });
  }

  // Normalize the sanitized value forward; the gateway does no other mutation.
  req.validatedScenario = trimmed;
  next();
}

module.exports = { validateAnalyzeInput };

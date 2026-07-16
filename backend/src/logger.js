"use strict";

const crypto = require("crypto");

// Anonymized request logging (CLAUDE.md Section 9).
//
// HARD RULE: raw scenario text is NEVER logged. Logged fields are limited to
// the request UUID, predicted domain/issue IDs, the two scores, language code,
// timestamp, and status. An optional SHA-256 hash of the scenario is included
// for de-duplication only — this is a technical measure, NOT a claim that the
// log is "anonymous".

function scenarioHash(scenario) {
  if (typeof scenario !== "string" || scenario.length === 0) return null;
  return crypto.createHash("sha256").update(scenario, "utf8").digest("hex");
}

// Build the anonymized log record from the ML response. Defensive: never
// touches scenario text; only reads the structured analysis fields.
function buildLogRecord({ requestId, scenario, statusCode, mlBody }) {
  const analysis = (mlBody && mlBody.analysis) || {};
  const domain = analysis.domain || {};
  const issue = analysis.issue || {};
  return {
    request_id: requestId,
    timestamp: new Date().toISOString(),
    status: statusCode,
    domain_id: domain.id || null,
    issue_id: issue.id || null,
    domain_confidence: typeof domain.confidence === "number" ? domain.confidence : null,
    issue_similarity_score:
      typeof issue.similarity_score === "number" ? issue.similarity_score : null,
    legal_information_status: (mlBody && mlBody.legal_information_status) || null,
    language: "en", // Phase 1 is English-only (CLAUDE.md 11.2)
    scenario_sha256: scenarioHash(scenario), // dedup only
  };
}

function logAnalysis(record) {
  // Structured line to stdout. A MySQL sink can replace this later without
  // changing callers (CLAUDE.md Section 16 — no premature DB dependency).
  console.log(JSON.stringify({ type: "analysis", ...record }));
}

module.exports = { buildLogRecord, logAnalysis, scenarioHash };

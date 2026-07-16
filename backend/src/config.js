"use strict";

// Central configuration. All values overridable by environment (.env).
// The gateway holds NO legal logic and NO legal constants — only transport
// and validation settings.

require("dotenv").config();

module.exports = {
  port: parseInt(process.env.PORT || "5000", 10),
  mlServiceUrl: process.env.ML_SERVICE_URL || "http://localhost:8000",
  mlTimeoutMs: parseInt(process.env.ML_TIMEOUT_MS || "10000", 10),

  // Input validation bounds — must match the ML service contract
  // (ml-service/app/schemas.py SCENARIO_MIN/MAX_LENGTH).
  scenarioMinLength: 20,
  scenarioMaxLength: 2000,

  // Rate limiting (CLAUDE.md Section 4.4): 10 requests / minute / IP.
  rateLimitWindowMs: 60 * 1000,
  rateLimitMax: 10,
};

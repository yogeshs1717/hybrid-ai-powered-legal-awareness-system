"use strict";

const rateLimit = require("express-rate-limit");
const config = require("./config");

// Rate limiting (CLAUDE.md Section 4.4): 10 requests / minute / IP.
// Returns HTTP 429 with the standard response contract's error shape.
const analyzeRateLimiter = rateLimit({
  windowMs: config.rateLimitWindowMs,
  max: config.rateLimitMax,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: "rate_limited",
    detail: "Too many requests. Please try again in a minute.",
  },
});

module.exports = { analyzeRateLimiter };

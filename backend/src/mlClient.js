"use strict";

const axios = require("axios");
const config = require("./config");

// HTTP client to the Python FastAPI ML service. This is the ONLY component that
// talks to the ML service. It is injected into the app (see app.js) so tests
// can substitute a fake without a live ML service.

function createMlClient({ baseUrl = config.mlServiceUrl, timeout = config.mlTimeoutMs } = {}) {
  const http = axios.create({ baseURL: baseUrl, timeout });

  return {
    // Forward an analysis request. Returns { status, data } from the ML service.
    // The gateway returns the ML response body UNCHANGED (contract preserved).
    async analyze({ scenario, requestId }) {
      const res = await http.post(
        "/analyze",
        { scenario, request_id: requestId },
        { validateStatus: () => true } // let the route map status codes itself
      );
      return { status: res.status, data: res.data };
    },

    async health() {
      const res = await http.get("/health", { validateStatus: () => true });
      return { status: res.status, data: res.data };
    },
  };
}

module.exports = { createMlClient };

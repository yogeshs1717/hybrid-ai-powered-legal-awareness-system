"use strict";

const test = require("node:test");
const assert = require("node:assert");
const request = require("supertest");
const { createApp } = require("../src/app");

// A canned ML response matching the locked contract (CLAUDE.md 8.1). The
// gateway must return this UNCHANGED for a successful analysis.
const ML_OK_BODY = {
  success: true,
  request_id: "will-be-overwritten-by-ml",
  analysis: {
    domain: { id: "cyber_fraud", display_name: "Cyber Fraud", confidence: 0.61, confidence_label: "Low" },
    issue: { id: "otp_fraud", display_name: "OTP Fraud", similarity_score: 0.8, issue_match_reason: "..." },
    scenario_signals: ["otp", "bank"],
  },
  legal_provisions: [{ section: "Section 66D", provision_relevance_rationale: "..." }],
  legal_information_status: "provisions_available",
  action_steps: ["a", "b"],
  portals: [],
  low_confidence_warning: true,
  needs_clarification: true,
  clarification_question: "…",
  disclaimer: "This information is for legal awareness only…",
};

// Fake ML client: records the last call so tests can assert what was forwarded.
function fakeMlClient(overrides = {}) {
  const calls = [];
  return {
    calls,
    async analyze(payload) {
      calls.push(payload);
      if (overrides.analyze) return overrides.analyze(payload);
      return { status: 200, data: ML_OK_BODY };
    },
    async health() {
      if (overrides.health) return overrides.health();
      return { status: 200, data: { status: "ok", classifier_mode: "trained" } };
    },
  };
}

const VALID = { scenario: "Someone called pretending to be my bank and asked for the OTP then money went." };

test("POST /api/analyze forwards to ML and returns the contract unchanged", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });
  const res = await request(app).post("/api/analyze").send(VALID);
  assert.strictEqual(res.status, 200);
  assert.deepStrictEqual(res.body, ML_OK_BODY); // body unchanged
  assert.strictEqual(ml.calls.length, 1);
  // A UUID request_id was generated and forwarded to the ML service.
  assert.match(ml.calls[0].requestId, /^[0-9a-f-]{36}$/);
  assert.strictEqual(ml.calls[0].scenario, VALID.scenario);
});

test("short scenario is rejected with HTTP 400 and never reaches the ML service", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });
  const res = await request(app).post("/api/analyze").send({ scenario: "help" });
  assert.strictEqual(res.status, 400);
  assert.strictEqual(res.body.error, "invalid_input");
  assert.strictEqual(ml.calls.length, 0);
});

test("missing/invalid scenario type is HTTP 400", async () => {
  const app = createApp({ mlClient: fakeMlClient() });
  const res = await request(app).post("/api/analyze").send({ scenario: 123 });
  assert.strictEqual(res.status, 400);
});

test("ML service validation status (400) is passed through", async () => {
  const ml = fakeMlClient({
    analyze: async () => ({ status: 400, data: { success: false, error: "invalid_input" } }),
  });
  const app = createApp({ mlClient: ml });
  const res = await request(app).post("/api/analyze").send(VALID);
  assert.strictEqual(res.status, 400);
});

test("ML service unreachable yields HTTP 503, not a fabricated answer", async () => {
  const ml = fakeMlClient({
    analyze: async () => {
      throw new Error("ECONNREFUSED");
    },
  });
  const app = createApp({ mlClient: ml });
  const res = await request(app).post("/api/analyze").send(VALID);
  assert.strictEqual(res.status, 503);
  assert.strictEqual(res.body.error, "ml_service_unavailable");
  assert.ok(res.body.request_id);
  assert.ok(!("legal_provisions" in res.body)); // no legal content invented
});

test("anonymized logging never emits the scenario text", async () => {
  const original = console.log;
  const lines = [];
  console.log = (...a) => lines.push(a.join(" "));
  try {
    const app = createApp({ mlClient: fakeMlClient() });
    await request(app).post("/api/analyze").send(VALID);
  } finally {
    console.log = original;
  }
  const joined = lines.join("\n");
  assert.ok(!joined.includes("asked for the OTP")); // raw scenario never logged
  const rec = lines.map((l) => { try { return JSON.parse(l); } catch { return {}; } })
                   .find((o) => o.type === "analysis");
  assert.ok(rec, "an analysis log record was emitted");
  assert.strictEqual(rec.domain_id, "cyber_fraud");
  assert.ok(rec.scenario_sha256 && rec.scenario_sha256.length === 64);
  assert.ok(!("scenario" in rec));
});

test("rate limiting returns HTTP 429 after the per-minute cap", async () => {
  const app = createApp({ mlClient: fakeMlClient() });
  const agent = request(app);
  let got429 = false;
  for (let i = 0; i < 12; i++) {
    const res = await agent.post("/api/analyze").send(VALID);
    if (res.status === 429) { got429 = true; break; }
  }
  assert.ok(got429, "expected a 429 within the first dozen requests (cap is 10)");
});

test("GET /api/health reports gateway ok and ML status", async () => {
  const app = createApp({ mlClient: fakeMlClient() });
  const res = await request(app).get("/api/health");
  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.body.gateway, "ok");
  assert.strictEqual(res.body.ml_service.reachable, true);
});

test("GET /api/domains lists the five approved domains", async () => {
  const app = createApp({ mlClient: fakeMlClient() });
  const res = await request(app).get("/api/domains");
  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.body.domains.length, 5);
});

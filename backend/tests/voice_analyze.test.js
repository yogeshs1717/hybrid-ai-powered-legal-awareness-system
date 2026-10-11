"use strict";

const test = require("node:test");
const assert = require("node:assert");
const request = require("supertest");
const { createApp } = require("../src/app");

const ML_OK_BODY = {
  success: true,
  request_id: "test-voice-req",
  analysis: {
    domain: { id: "cyber_fraud", display_name: "Cyber Fraud", confidence: 0.85, confidence_label: "High" },
    issue: { id: "otp_fraud", display_name: "OTP Fraud", similarity_score: 0.88, issue_match_reason: "..." },
    scenario_signals: ["otp", "bank"],
  },
  legal_provisions: [{ section: "Section 66D", provision_relevance_rationale: "..." }],
  legal_information_status: "provisions_available",
  action_steps: ["Step 1", "Step 2"],
  portals: [],
  disclaimer: "This information is for legal awareness only.",
};

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
      return { status: 200, data: { status: "ok" } };
    },
  };
}

test("Voice input workflow: English transcript is accepted and analyzed", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  // Simulated voice transcript in English (user reviewed and submitted)
  const voiceTranscript = "Someone called pretending to be bank manager and asked for OTP then money deducted";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: voiceTranscript });

  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.body.success, true);
  assert.strictEqual(ml.calls.length, 1);
  assert.strictEqual(ml.calls[0].scenario, voiceTranscript);
});

test("Voice input workflow: User-edited transcript is accepted and analyzed", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  // User edited the transcription before clicking analyze (e.g. fixed bank name)
  const correctedTranscript = "An unknown caller claiming to be from SBI asked for my card OTP and Rs 50000 was debited";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: correctedTranscript });

  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.body.success, true);
  assert.strictEqual(ml.calls[0].scenario, correctedTranscript);
});

test("Voice input workflow: Hindi transcript (Devanagari) is detected and bridged to ML", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  // Hindi voice transcript in Devanagari script
  const hindiTranscript = "किसी ने मुझे फोन करके बैंक मैनेजर बताया और ओटीपी मांगा, जिसके बाद मेरे पैसे कट गए";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: hindiTranscript });

  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.headers["x-detected-language"], "hi");
  assert.strictEqual(ml.calls.length, 1);
  // ML pipeline received the scenario (translated or bridged)
  assert.ok(ml.calls[0].scenario.length >= 10);
});

test("Voice input workflow: Kannada transcript is detected and bridged to ML", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  // Kannada voice transcript in Kannada script
  const kannadaTranscript = "ಯಾರೋ ನನಗೆ ಕರೆ ಮಾಡಿ ಬ್ಯಾಂಕ್ ಮ್ಯಾನೇಜರ್ ಎಂದು ಹೇಳಿ ಒಟಿಪಿ ಕೇಳಿದರು, ನಂತರ ನನ್ನ ಹಣ ಕಡಿತವಾಯಿತು";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: kannadaTranscript });

  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.headers["x-detected-language"], "kn");
  assert.strictEqual(ml.calls.length, 1);
  assert.ok(ml.calls[0].scenario.length >= 10);
});

test("Regression test: Typed English complaints continue working unchanged", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  const typedComplaint = "I bought a refrigerator online and it stopped working after two days but seller refused refund.";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: typedComplaint });

  assert.strictEqual(res.status, 200);
  assert.strictEqual(ml.calls.length, 1);
  assert.strictEqual(ml.calls[0].scenario, typedComplaint);
});

test("Regression test: Transcripts under 20 characters are rejected with HTTP 400", async () => {
  const ml = fakeMlClient();
  const app = createApp({ mlClient: ml });

  const tooShort = "short voice note";

  const res = await request(app)
    .post("/api/analyze")
    .send({ scenario: tooShort });

  assert.strictEqual(res.status, 400);
  assert.strictEqual(ml.calls.length, 0); // never reaches ML
});

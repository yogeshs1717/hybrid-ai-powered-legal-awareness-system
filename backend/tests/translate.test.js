"use strict";

const test = require("node:test");
const assert = require("node:assert");
const request = require("supertest");
const { createApp } = require("../src/app");
const { detectScript, translateText } = require("../src/translator");

test("detectScript accurately identifies Hindi, Kannada, and English scripts", () => {
  assert.strictEqual(detectScript("Hello world, this is a test."), "en");
  assert.strictEqual(detectScript("नमस्ते, यह एक परीक्षण है।"), "hi");
  assert.strictEqual(detectScript("ನಮಸ್ಕಾರ, ಇದು ಒಂದು ಪರೀಕ್ಷೆ."), "kn");
});

test("POST /api/translate validates input and returns 400 if text is missing", async () => {
  const app = createApp();
  const res = await request(app).post("/api/translate").send({});
  assert.strictEqual(res.status, 400);
  assert.strictEqual(res.body.success, false);
});

test("POST /api/translate translates text to Hindi and Kannada", async () => {
  const app = createApp();
  const resHi = await request(app)
    .post("/api/translate")
    .send({ text: "Consumer Protection", target: "hi" });
  assert.strictEqual(resHi.status, 200);
  assert.strictEqual(resHi.body.success, true);
  assert.ok(typeof resHi.body.translated === "string");
  assert.ok(resHi.body.translated.length > 0);

  const resKn = await request(app)
    .post("/api/translate")
    .send({ text: "Consumer Protection", target: "kn" });
  assert.strictEqual(resKn.status, 200);
  assert.strictEqual(resKn.body.success, true);
  assert.ok(typeof resKn.body.translated === "string");
  assert.ok(resKn.body.translated.length > 0);
});

test("POST /api/translate translates an array of texts", async () => {
  const app = createApp();
  const res = await request(app)
    .post("/api/translate")
    .send({ texts: ["Cyber Fraud", "Action Steps"], target: "hi" });
  assert.strictEqual(res.status, 200);
  assert.strictEqual(res.body.success, true);
  assert.ok(Array.isArray(res.body.translated));
  assert.strictEqual(res.body.translated.length, 2);
});

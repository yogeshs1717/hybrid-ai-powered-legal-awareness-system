"use strict";

const { createApp } = require("./app");
const config = require("./config");

// Real entrypoint. Wires the default (axios) ML client and starts listening.
const app = createApp();

const server = app.listen(config.port, () => {
  // eslint-disable-next-line no-console
  console.log(
    JSON.stringify({
      type: "startup",
      message: "API gateway listening",
      port: config.port,
      ml_service_url: config.mlServiceUrl,
    })
  );
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    // eslint-disable-next-line no-console
    console.error(
      `\n[FATAL ERROR] Port ${config.port} is already in use by another application.\n` +
      `To resolve:\n` +
      `1. Stop the process holding port ${config.port} (e.g.: fuser -k ${config.port}/tcp)\n` +
      `2. Or start LegalLens gateway on another port: PORT=5001 npm run dev\n`
    );
  } else {
    // eslint-disable-next-line no-console
    console.error("[FATAL ERROR] Gateway server failure:", err);
  }
  process.exit(1);
});


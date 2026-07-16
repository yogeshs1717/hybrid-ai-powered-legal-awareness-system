"use strict";

const { createApp } = require("./app");
const config = require("./config");

// Real entrypoint. Wires the default (axios) ML client and starts listening.
const app = createApp();

app.listen(config.port, () => {
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

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// LegalLens frontend build config.
// The dev proxy forwards /api to the Node.js gateway (port 5000) so the browser
// talks to a same-origin path in development — no CORS juggling, and the scenario
// text never leaves the POST body (CLAUDE.md Section 9).
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: process.env.VITE_GATEWAY_URL || "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});

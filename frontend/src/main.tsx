import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { MotionGlobalConfig } from "framer-motion";
import App from "./App";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { QueryProvider } from "@/providers/QueryProvider";
import "./index.css";

// Dev/test-only escape hatch: `?no-anim` completes all Framer animations
// instantly so automated checks can assert final DOM states in environments
// that throttle requestAnimationFrame (hidden tabs, CI). Stripped from
// production behavior by the DEV guard.
if (import.meta.env.DEV && new URLSearchParams(location.search).has("no-anim")) {
  MotionGlobalConfig.skipAnimations = true;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider>
      <QueryProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryProvider>
    </ThemeProvider>
  </React.StrictMode>,
);

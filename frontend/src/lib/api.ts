import type { AnalyzeResponse } from "@/types/contract";

/*
  Gateway client. Talks ONLY to the Node.js gateway (default same-origin /api,
  proxied to :5000 in dev) — never directly to the FastAPI ML service.

  Status handling mirrors the gateway contract exactly:
    200  -> success body (INCLUDING low-confidence; those are flags, not errors)
    400  -> input validation failure
    429  -> rate limited (10 req/min/IP)
    503  -> ML service unreachable (never a fabricated answer)
*/

const BASE = import.meta.env.VITE_API_BASE ?? "/api";

export type AnalyzeErrorKind =
  | "invalid_input"
  | "rate_limited"
  | "service_unavailable"
  | "network"
  | "unknown";

export class AnalyzeError extends Error {
  kind: AnalyzeErrorKind;
  status?: number;
  constructor(kind: AnalyzeErrorKind, message: string, status?: number) {
    super(message);
    this.name = "AnalyzeError";
    this.kind = kind;
    this.status = status;
  }
}

/** Privacy (CLAUDE.md Section 9): scenario travels in the POST body only. */
export async function analyzeScenario(
  scenario: string,
  signal?: AbortSignal,
): Promise<AnalyzeResponse> {
  const timeoutMs = 15000;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  if (signal) {
    signal.addEventListener("abort", () => controller.abort());
  }

  let res: Response;
  try {
    res = await fetch(`${BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario }),
      signal: controller.signal,
    });
  } catch (e) {
    if ((e as Error).name === "AbortError") {
      if (signal?.aborted) throw e;
      throw new AnalyzeError(
        "service_unavailable",
        "Analysis timed out. Please check that the server is responding and try again.",
        504,
      );
    }
    throw new AnalyzeError(
      "network",
      "Could not reach LegalLens. Please check your connection.",
    );
  } finally {
    clearTimeout(timeoutId);
  }

  if (res.ok) {
    return (await res.json()) as AnalyzeResponse;
  }

  let detail = "";
  try {
    const body = await res.json();
    detail = body?.detail || body?.error || "";
  } catch {
    /* non-JSON error body */
  }

  switch (res.status) {
    case 400:
      throw new AnalyzeError(
        "invalid_input",
        detail || "Please describe your situation in a bit more detail.",
        400,
      );
    case 429:
      throw new AnalyzeError(
        "rate_limited",
        "You're going a little fast. Please wait a moment and try again.",
        429,
      );
    case 503:
      throw new AnalyzeError(
        "service_unavailable",
        "The analysis service is temporarily unavailable. Please try again shortly.",
        503,
      );
    default:
      throw new AnalyzeError(
        "unknown",
        detail || "Something went wrong. Please try again.",
        res.status,
      );
  }
}

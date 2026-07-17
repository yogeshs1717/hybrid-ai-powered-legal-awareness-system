import { useMutation } from "@tanstack/react-query";
import { analyzeScenario, AnalyzeError } from "@/lib/api";
import type { AnalyzeResponse } from "@/types/contract";

/**
 * Drives the POST /api/analyze lifecycle. Low-confidence responses arrive on
 * the SUCCESS path (HTTP 200) — the caller inspects the flags on the body.
 */
export function useAnalyze() {
  return useMutation<AnalyzeResponse, AnalyzeError, string>({
    mutationFn: (scenario: string) => analyzeScenario(scenario),
  });
}

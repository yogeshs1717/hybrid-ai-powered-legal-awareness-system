import { useMutation } from "@tanstack/react-query";
import { analyzeScenario, AnalyzeError } from "@/lib/api";
import type { AnalyzeResponse } from "@/types/contract";

/**
 * Drives the POST /api/analyze lifecycle. Low-confidence responses arrive on
 * the SUCCESS path (HTTP 200) — the caller inspects the flags on the body.
 */
export type AnalyzeMutationInput = string | { scenario: string; language?: string };

export function useAnalyze() {
  return useMutation<AnalyzeResponse, AnalyzeError, AnalyzeMutationInput>({
    mutationFn: (input: AnalyzeMutationInput) => {
      if (typeof input === "string") {
        return analyzeScenario(input);
      }
      return analyzeScenario(input.scenario, undefined, input.language);
    },
  });
}


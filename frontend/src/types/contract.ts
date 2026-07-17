/*
  Typed mirror of the ML/API response contract (CLAUDE.md Section 8.1).
  The frontend holds NO legal logic (Section 4.4) — it only renders these
  fields exactly as the gateway returns them. Keep this file in lockstep with
  the backend contract; do not add computed legal meaning here.
*/

export type ConfidenceLabel = "High" | "Medium" | "Low";

export type LegalInformationStatus =
  | "provisions_available"
  | "no_verified_provision_available";

export interface DomainAnalysis {
  id: string;
  display_name: string;
  /** Logistic Regression predict_proba() — "model confidence", never legal certainty. */
  confidence: number;
  confidence_label: ConfidenceLabel;
}

export interface IssueAnalysis {
  /** Null when no issue could be detected (e.g. no prototypes exist yet for
   *  the predicted domain) — the UI must skip the issue card in that case. */
  id: string | null;
  display_name: string | null;
  /**
   * Cosine similarity against curated prototypes. NEVER surfaced to citizens as
   * confidence/certainty (CLAUDE.md Section 6.2). Retained only for a dev debug
   * overlay — the citizen UI does not display this number.
   */
  similarity_score: number | null;
  /** Layer A — generated scenario→issue match reason (CLAUDE.md Section 6.7). */
  issue_match_reason: string | null;
}

export interface Analysis {
  domain: DomainAnalysis;
  issue: IssueAnalysis;
  scenario_signals: string[];
}

export interface OfficialSource {
  name: string;
  url: string | null;
}

export interface LegalProvision {
  act_id: string;
  act: string;
  section: string;
  title: string;
  simplified_explanation: string;
  /** Layer B — curated, human-authored issue→provision rationale (Section 6.7). */
  provision_relevance_rationale: string;
  official_source: OfficialSource;
}

export type PortalPriority = "immediate" | "primary" | "secondary";

export interface Portal {
  name: string;
  official_url: string;
  purpose: string;
  priority: PortalPriority;
}

/** The success-path body returned by POST /api/analyze (HTTP 200). */
export interface AnalyzeResponse {
  success: true;
  request_id: string;
  analysis: Analysis;
  legal_provisions: LegalProvision[];
  legal_information_status: LegalInformationStatus;
  action_steps: string[];
  portals: Portal[];
  low_confidence_warning: boolean;
  needs_clarification: boolean;
  clarification_question: string | null;
  disclaimer: string;
}

/** Error body shape used by the gateway for 400 / 429 / 503 responses. */
export interface GatewayError {
  success: false;
  request_id?: string;
  error: string;
  detail?: string;
}

export interface DomainSummary {
  id: string;
  display_name: string;
}

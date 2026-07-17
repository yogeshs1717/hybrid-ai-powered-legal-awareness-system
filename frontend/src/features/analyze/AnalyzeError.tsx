import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CloudOff, Clock, TriangleAlert, RotateCcw } from "lucide-react";
import type { AnalyzeError as AnalyzeErrorType } from "@/lib/api";

/*
  Honest error surfaces mapped from the gateway contract. Crucially, a 503 shows
  "temporarily unavailable" — LegalLens never fabricates a legal answer when the
  analysis service is down (mirrors the gateway's own guarantee).
*/
export function AnalyzeErrorCard({
  error,
  onRetry,
}: {
  error: AnalyzeErrorType;
  onRetry: () => void;
}) {
  const map = {
    rate_limited: {
      icon: Clock,
      title: "Just a moment",
    },
    service_unavailable: {
      icon: CloudOff,
      title: "Analysis service is unavailable",
    },
    network: {
      icon: CloudOff,
      title: "Connection problem",
    },
    invalid_input: {
      icon: TriangleAlert,
      title: "Let's adjust that",
    },
    unknown: {
      icon: TriangleAlert,
      title: "Something went wrong",
    },
  } as const;

  const kind = (map as Record<string, (typeof map)[keyof typeof map]>)[error.kind] ??
    map.unknown;
  const Icon = kind.icon;

  return (
    <Card className="mx-auto max-w-xl p-6 sm:p-8 text-center">
      <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-destructive/12 text-destructive">
        <Icon className="h-6 w-6" aria-hidden />
      </span>
      <h3 className="mt-4 font-display text-xl font-semibold text-foreground">
        {kind.title}
      </h3>
      <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-muted-foreground text-pretty">
        {error.message}
      </p>
      <div className="mt-6">
        <Button onClick={onRetry} variant="secondary">
          <RotateCcw className="h-4 w-4" /> Try again
        </Button>
      </div>
    </Card>
  );
}

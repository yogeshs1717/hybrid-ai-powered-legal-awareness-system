import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { LensMark } from "@/components/brand/LensMark";

export function NotFoundPage() {
  return (
    <div className="container flex min-h-[70dvh] flex-col items-center justify-center py-20 text-center">
      <LensMark className="h-14 w-14 opacity-80" />
      <h1 className="mt-6 font-display text-4xl font-semibold tracking-tight">
        Nothing to see here
      </h1>
      <p className="mt-3 max-w-sm text-muted-foreground text-pretty">
        We couldn't find that page. Let's get you back to somewhere useful.
      </p>
      <div className="mt-8 flex flex-col gap-3 sm:flex-row">
        <Button asChild>
          <Link to="/">Back to home</Link>
        </Button>
        <Button asChild variant="secondary">
          <Link to="/analyze">Analyze a situation</Link>
        </Button>
      </div>
    </div>
  );
}

import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import { TooltipProvider } from "@/components/ui/tooltip";
import { RootLayout } from "@/components/layout/RootLayout";
import { LandingPage } from "@/pages/LandingPage";
import { NotFoundPage } from "@/pages/NotFoundPage";

// Analyzer and How-it-works are route-split so the landing bundle stays light.
const AnalyzePage = lazy(() =>
  import("@/pages/AnalyzePage").then((m) => ({ default: m.AnalyzePage })),
);
const HowItWorksPage = lazy(() =>
  import("@/pages/HowItWorksPage").then((m) => ({ default: m.HowItWorksPage })),
);

export default function App() {
  return (
    <TooltipProvider delayDuration={200}>
      <Routes>
        <Route element={<RootLayout />}>
          <Route index element={<LandingPage />} />
          <Route
            path="analyze"
            element={
              <Suspense fallback={null}>
                <AnalyzePage />
              </Suspense>
            }
          />
          <Route
            path="how-it-works"
            element={
              <Suspense fallback={null}>
                <HowItWorksPage />
              </Suspense>
            }
          />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </TooltipProvider>
  );
}

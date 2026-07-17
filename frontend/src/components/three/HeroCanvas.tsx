import { lazy, Suspense, useEffect, useRef, useState } from "react";
import { useReducedMotion } from "framer-motion";
import { HeroFallback } from "./HeroFallback";

// The 3D scene (three.js + R3F) is code-split so it never enters the analyzer
// or initial landing critical path.
const HeroScene = lazy(() => import("./HeroScene"));

/*
  Decides whether the WebGL hero runs at all:
   - prefers-reduced-motion  -> static fallback, no canvas (accessibility)
   - viewport < 768px        -> static fallback; phones never download three.js
   - offscreen               -> unmount the canvas (stop rendering / save battery)
   - otherwise               -> lazy-load and render the scene over the fallback
*/
export function HeroCanvas() {
  const reduce = useReducedMotion();
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [wideEnough, setWideEnough] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(min-width: 768px)");
    const update = () => setWideEnough(mq.matches);
    update();
    // Listen to both: some embedded/emulated contexts don't dispatch
    // MediaQueryList "change" events reliably, but always fire "resize".
    mq.addEventListener("change", update);
    window.addEventListener("resize", update, { passive: true });
    return () => {
      mq.removeEventListener("change", update);
      window.removeEventListener("resize", update);
    };
  }, []);

  const enabled = !reduce && wideEnough;

  useEffect(() => {
    if (!enabled) return;
    const el = ref.current;
    if (!el) return;
    // Seed visibility synchronously so the initial mount never depends on the
    // observer firing (some embedded/throttled contexts delay IO callbacks).
    // The observer then only handles pausing when scrolled offscreen.
    const rect = el.getBoundingClientRect();
    setVisible(rect.bottom > 0 && rect.top < window.innerHeight);
    const io = new IntersectionObserver(
      ([entry]) => setVisible(entry.isIntersecting),
      { threshold: 0.05 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [enabled]);

  return (
    <div ref={ref} className="absolute inset-0">
      {/* Fallback is always present; the canvas fades in on top when ready. */}
      <HeroFallback />
      {enabled && visible && (
        <Suspense fallback={null}>
          <HeroScene />
        </Suspense>
      )}
    </div>
  );
}

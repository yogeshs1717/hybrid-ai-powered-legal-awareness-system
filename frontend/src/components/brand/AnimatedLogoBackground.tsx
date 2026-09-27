import { useEffect, useState } from "react";
import { motion, useMotionValue, useSpring, useReducedMotion } from "framer-motion";

export function AnimatedLogoBackground() {
  const reduce = useReducedMotion();
  const [mounted, setMounted] = useState(false);

  // Mouse parallax motion values
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  // Smooth springs for gentle, fluid motion
  const springX = useSpring(mouseX, { stiffness: 45, damping: 25 });
  const springY = useSpring(mouseY, { stiffness: 45, damping: 25 });
  const springXSlow = useSpring(mouseX, { stiffness: 20, damping: 30 });
  const springYSlow = useSpring(mouseY, { stiffness: 20, damping: 30 });

  useEffect(() => {
    setMounted(true);
    const handleMouseMove = (e: MouseEvent) => {
      const { innerWidth, innerHeight } = window;
      const x = (e.clientX / innerWidth - 0.5) * 40;
      const y = (e.clientY / innerHeight - 0.5) * 40;
      mouseX.set(x);
      mouseY.set(y);
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [mouseX, mouseY]);

  if (!mounted) return null;

  return (
    <div
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 -z-10 overflow-hidden select-none"
    >
      {/* ---------- Central Ambient Glow Aura ---------- */}
      <motion.div
        animate={
          reduce
            ? {}
            : {
                scale: [1, 1.15, 1],
                opacity: [0.25, 0.4, 0.25],
              }
        }
        transition={{
          duration: 9,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[32rem] w-[32rem] sm:h-[45rem] sm:w-[45rem] rounded-full bg-gradient-to-tr from-primary/20 via-blue-500/10 to-indigo-500/20 blur-3xl"
      />

      {/* ---------- Secondary Counter-Glow (Warm Indigo) ---------- */}
      <motion.div
        animate={
          reduce
            ? {}
            : {
                scale: [1.1, 0.95, 1.1],
                opacity: [0.15, 0.3, 0.15],
              }
        }
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-1/3 right-1/4 h-[24rem] w-[24rem] rounded-full bg-indigo-500/15 blur-3xl"
      />

      {/* ---------- Primary Floating Giant Logo (Hero Watermark) ---------- */}
      <motion.div
        style={{
          x: reduce ? 0 : springX,
          y: reduce ? 0 : springY,
        }}
        className="absolute top-[8%] left-1/2 -translate-x-1/2 sm:top-[6%]"
      >
        <motion.div
          animate={
            reduce
              ? {}
              : {
                  y: [-12, 14, -12],
                  rotate: [-2, 3, -2],
                  scale: [0.98, 1.02, 0.98],
                }
          }
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="relative h-[340px] w-[340px] sm:h-[500px] sm:w-[500px] opacity-[0.22] dark:opacity-[0.28] transition-opacity duration-500"
        >
          {/* Outer Dashed Orbit Ring 1 (Rotates Clockwise) */}
          <motion.div
            animate={reduce ? {} : { rotate: 360 }}
            transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
            className="absolute inset-[-24px] rounded-full border border-dashed border-primary/30 dark:border-primary/25"
          />

          {/* Outer Dashed Orbit Ring 2 (Rotates Counter-Clockwise) */}
          <motion.div
            animate={reduce ? {} : { rotate: -360 }}
            transition={{ duration: 45, repeat: Infinity, ease: "linear" }}
            className="absolute inset-[-48px] rounded-full border border-dotted border-indigo-400/25 dark:border-indigo-400/20"
          />

          {/* SVG Logo Graphic */}
          <svg
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="h-full w-full drop-shadow-[0_0_35px_rgba(59,130,246,0.3)]"
          >
            <defs>
              <linearGradient id="logo-rim-grad" x1="15" y1="10" x2="75" y2="80" gradientUnits="userSpaceOnUse">
                <stop stopColor="hsl(var(--primary))" stopOpacity="0.9" />
                <stop offset="0.5" stopColor="#60a5fa" stopOpacity="0.8" />
                <stop offset="1" stopColor="#818cf8" stopOpacity="0.7" />
              </linearGradient>

              <radialGradient id="logo-lens-glass" cx="42%" cy="40%" r="55%">
                <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.25" />
                <stop offset="60%" stopColor="#3b82f6" stopOpacity="0.08" />
                <stop offset="100%" stopColor="transparent" stopOpacity="0" />
              </radialGradient>

              <linearGradient id="line-glow" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity="0.9" />
                <stop offset="50%" stopColor="#93c5fd" stopOpacity="1" />
                <stop offset="100%" stopColor="#6366f1" stopOpacity="0.8" />
              </linearGradient>
            </defs>

            {/* Lens Glass Body */}
            <circle cx="42" cy="42" r="28" fill="url(#logo-lens-glass)" />

            {/* Primary Glowing Lens Rim */}
            <circle
              cx="42"
              cy="42"
              r="28"
              stroke="url(#logo-rim-grad)"
              strokeWidth="4"
              className="filter drop-shadow-sm"
            />

            {/* Inner Concentric Rim Accent */}
            <circle
              cx="42"
              cy="42"
              r="24"
              stroke="hsl(var(--primary))"
              strokeWidth="0.8"
              strokeOpacity="0.3"
              strokeDasharray="4 3"
            />

            {/* Clarity Lines (Document stripes inside lens) */}
            <g stroke="url(#line-glow)" strokeLinecap="round">
              <motion.line
                animate={reduce ? {} : { strokeOpacity: [0.6, 1, 0.6] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                x1="28"
                y1="34"
                x2="56"
                y2="34"
                strokeWidth="3.5"
              />
              <motion.line
                animate={reduce ? {} : { strokeOpacity: [0.5, 0.95, 0.5] }}
                transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut", delay: 0.3 }}
                x1="28"
                y1="42.5"
                x2="52"
                y2="42.5"
                strokeWidth="3.5"
              />
              <motion.line
                animate={reduce ? {} : { strokeOpacity: [0.4, 0.9, 0.4] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
                x1="28"
                y1="51"
                x2="46"
                y2="51"
                strokeWidth="3.5"
              />
            </g>

            {/* Magnifying Glass Handle */}
            <path
              d="M62 62 L82 82"
              stroke="url(#logo-rim-grad)"
              strokeWidth="6"
              strokeLinecap="round"
            />

            {/* Handle Grip Accent Ring */}
            <line
              x1="70"
              y1="70"
              x2="74"
              y2="74"
              stroke="#ffffff"
              strokeOpacity="0.4"
              strokeWidth="4.5"
              strokeLinecap="round"
            />
          </svg>
        </motion.div>
      </motion.div>

      {/* ---------- Floating Satellite Logo 1 (Top Left) ---------- */}
      <motion.div
        style={{
          x: reduce ? 0 : springXSlow,
          y: reduce ? 0 : springYSlow,
        }}
        className="absolute top-[12%] left-[8%] sm:left-[14%]"
      >
        <motion.div
          animate={
            reduce
              ? {}
              : {
                  y: [0, -18, 0],
                  rotate: [0, 20, 0],
                  scale: [1, 1.08, 1],
                }
          }
          transition={{
            duration: 9,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="h-16 w-16 sm:h-24 sm:w-24 opacity-15 dark:opacity-20 blur-[0.5px]"
        >
          <svg viewBox="0 0 40 40" fill="none" className="h-full w-full">
            <circle cx="17" cy="17" r="11" stroke="hsl(var(--primary))" strokeWidth="2.5" />
            <line x1="12" y1="14" x2="22" y2="14" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" />
            <line x1="12" y1="17.5" x2="20.5" y2="17.5" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" />
            <line x1="12" y1="21" x2="18" y2="21" stroke="hsl(var(--primary))" strokeWidth="2" strokeLinecap="round" />
            <path d="M25 25 L32 32" stroke="hsl(var(--primary))" strokeWidth="3" strokeLinecap="round" />
          </svg>
        </motion.div>
      </motion.div>

      {/* ---------- Floating Satellite Logo 2 (Bottom Right) ---------- */}
      <motion.div
        style={{
          x: reduce ? 0 : springX,
          y: reduce ? 0 : springY,
        }}
        className="absolute top-[52%] right-[6%] sm:right-[12%]"
      >
        <motion.div
          animate={
            reduce
              ? {}
              : {
                  y: [0, 22, 0],
                  rotate: [0, -18, 0],
                  scale: [0.95, 1.05, 0.95],
                }
          }
          transition={{
            duration: 11,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
          className="h-20 w-20 sm:h-28 sm:w-28 opacity-15 dark:opacity-20 blur-[0.5px]"
        >
          <svg viewBox="0 0 40 40" fill="none" className="h-full w-full">
            <circle cx="17" cy="17" r="11" stroke="#818cf8" strokeWidth="2.5" />
            <line x1="12" y1="14" x2="22" y2="14" stroke="#818cf8" strokeWidth="2" strokeLinecap="round" />
            <line x1="12" y1="17.5" x2="20.5" y2="17.5" stroke="#818cf8" strokeWidth="2" strokeLinecap="round" />
            <line x1="12" y1="21" x2="18" y2="21" stroke="#818cf8" strokeWidth="2" strokeLinecap="round" />
            <path d="M25 25 L32 32" stroke="#818cf8" strokeWidth="3" strokeLinecap="round" />
          </svg>
        </motion.div>
      </motion.div>

      {/* ---------- Subtle Drifting Ambient Light Beam ---------- */}
      <motion.div
        animate={
          reduce
            ? {}
            : {
                x: [-30, 30, -30],
                opacity: [0.08, 0.16, 0.08],
              }
        }
        transition={{
          duration: 14,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-0 left-1/3 h-[500px] w-[200px] -rotate-45 bg-gradient-to-b from-blue-400/20 via-primary/10 to-transparent blur-3xl"
      />
    </div>
  );
}

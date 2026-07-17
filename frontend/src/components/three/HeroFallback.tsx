/*
  Static, dependency-free hero backdrop. Shown when the viewer prefers reduced
  motion, on small viewports (phones never download three.js), while the 3D
  scene lazy-loads, or as the base layer beneath it. Pure CSS — a quiet lens
  glow high-right, echoing the 3D composition so the swap is seamless.
*/
export function HeroFallback() {
  return (
    <div aria-hidden className="absolute inset-0 overflow-hidden">
      {/* soft jade bloom, high-right — mirrors the 3D lens position */}
      <div className="absolute right-[-8%] top-[6%] h-[34rem] w-[34rem] rounded-full bg-[radial-gradient(circle,hsl(var(--primary)/0.14),transparent_62%)] blur-2xl md:right-[2%]" />
      {/* faint lens rings */}
      <div className="absolute right-[4%] top-[16%] hidden h-[18rem] w-[18rem] rounded-full border border-primary/15 md:block" />
      <div className="absolute right-[7%] top-[22%] hidden h-[13rem] w-[13rem] rounded-full border border-accent/10 md:block" />
      {/* warm brass counter-glow, low-left */}
      <div className="absolute bottom-[-10%] left-[-6%] h-[26rem] w-[26rem] rounded-full bg-[radial-gradient(circle,hsl(var(--accent)/0.10),transparent_58%)] blur-2xl" />
    </div>
  );
}

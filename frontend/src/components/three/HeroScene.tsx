import { useMemo, useRef } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Float } from "@react-three/drei";
import * as THREE from "three";

/*
  LegalLens hero — quiet, atmospheric, law-themed.

  Design intent (approved refinement): the scene SUPPORTS the headline, it does
  not compete with it. A slender glass lens drifts high-right of the composition,
  slightly behind the content plane; faint "law lines" (an abstract statute page)
  recede into fog. The lines seen through the lens resolve brighter — the brand
  promise, "See the law more clearly", rendered literally but softly.

  Elegance levers used here: depth fog, low-emissive materials, slow drift,
  restrained pointer parallax. No particles, no bloom, no spectacle.
  Self-contained lighting (no HDR fetch); DPR capped for low-end devices.
*/

const JADE = "#4fd6a0";
const BRASS = "#e7c979";
const INK = "#0b120f";

/** Faint horizontal "law lines" — a statute page rendered abstractly. */
function LawLines({
  crisp = false,
  count = 7,
  width = 5,
  gap = 0.42,
}: {
  crisp?: boolean;
  count?: number;
  width?: number;
  gap?: number;
}) {
  const rows = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        y: (i - (count - 1) / 2) * gap,
        // Lines taper like justified text; deterministic, not random.
        w: width * (0.55 + 0.45 * Math.abs(Math.cos(i * 1.3))),
      })),
    [count, width, gap],
  );
  return (
    <group>
      {rows.map(({ y, w }, i) => (
        <mesh key={i} position={[(-width + w) / 2 + 0.1, y, 0]}>
          <planeGeometry args={[w, crisp ? 0.05 : 0.035]} />
          <meshBasicMaterial
            color={crisp ? BRASS : "#31584a"}
            transparent
            opacity={crisp ? 0.75 : 0.22}
            depthWrite={false}
          />
        </mesh>
      ))}
    </group>
  );
}

function LensRig() {
  const group = useRef<THREE.Group>(null);
  const lens = useRef<THREE.Group>(null);
  const { pointer } = useThree();

  useFrame((state, delta) => {
    if (!group.current || !lens.current) return;
    // Very slow drift — ambience, not attention.
    group.current.rotation.z += delta * 0.018;
    // Restrained pointer parallax, eased. The lens leans, never chases.
    const tx = 2.05 + pointer.x * 0.28;
    const ty = 0.55 + pointer.y * 0.2;
    lens.current.position.x += (tx - lens.current.position.x) * 0.035;
    lens.current.position.y += (ty - lens.current.position.y) * 0.035;
    const t = state.clock.elapsedTime;
    lens.current.rotation.z = Math.sin(t * 0.22) * 0.05;
  });

  return (
    <group ref={group}>
      {/* The faint world of law, receding into fog behind everything. */}
      <group position={[-0.6, 0.1, -2.6]} rotation={[0, 0.12, 0]}>
        <LawLines count={11} width={9} gap={0.5} />
      </group>

      <Float speed={0.8} rotationIntensity={0.12} floatIntensity={0.28}>
        {/* High-right, behind the content plane — supporting, not dominating. */}
        <group ref={lens} position={[2.05, 0.55, -0.9]} scale={0.82}>
          {/* Lines resolved crisply within the lens. */}
          <group position={[0, 0, -0.12]} scale={0.42}>
            <LawLines crisp count={5} width={3.6} />
          </group>

          {/* Lens glass — barely-there jade tint. */}
          <mesh>
            <circleGeometry args={[1.35, 64]} />
            <meshPhysicalMaterial
              color={JADE}
              transparent
              opacity={0.08}
              roughness={0.2}
              metalness={0}
              transmission={0.5}
              thickness={0.4}
              ior={1.25}
              depthWrite={false}
            />
          </mesh>

          {/* Rim — thin, low-emissive jade with a whisper of brass. */}
          <mesh>
            <torusGeometry args={[1.35, 0.038, 20, 96]} />
            <meshStandardMaterial
              color={JADE}
              emissive={JADE}
              emissiveIntensity={0.32}
              roughness={0.35}
              metalness={0.55}
            />
          </mesh>
          <mesh>
            <torusGeometry args={[1.42, 0.012, 12, 96]} />
            <meshStandardMaterial
              color={BRASS}
              emissive={BRASS}
              emissiveIntensity={0.28}
              roughness={0.45}
              metalness={0.65}
              transparent
              opacity={0.8}
            />
          </mesh>

          {/* Handle. */}
          <mesh position={[1.5, -1.5, 0]} rotation={[0, 0, Math.PI / 4]}>
            <capsuleGeometry args={[0.05, 1.0, 8, 16]} />
            <meshStandardMaterial
              color={BRASS}
              emissive={BRASS}
              emissiveIntensity={0.18}
              roughness={0.4}
              metalness={0.65}
            />
          </mesh>
        </group>
      </Float>
    </group>
  );
}

export default function HeroScene() {
  return (
    <Canvas
      aria-hidden
      dpr={[1, 1.5]}
      camera={{ position: [0, 0, 6], fov: 42 }}
      gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
      className="!absolute inset-0"
    >
      {/* Depth: everything melts into the page's ink as it recedes. */}
      <fog attach="fog" args={[INK, 4.5, 11]} />
      <ambientLight intensity={0.4} />
      <directionalLight position={[3, 4, 5]} intensity={0.8} />
      <pointLight position={[-4, -2, 3]} intensity={22} color={JADE} />
      <pointLight position={[4.5, 3, 2]} intensity={16} color={BRASS} />
      <LensRig />
    </Canvas>
  );
}

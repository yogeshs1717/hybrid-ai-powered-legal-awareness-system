# LegalLens — Frontend

> **See the law more clearly.**
> React frontend for the Smart Legal Intelligence System (Phase 1).

A premium, dark-first, mobile-first web experience that lets an Indian citizen
describe a real-life situation in plain language and receive: the relevant area
of law, curated legal provisions (verified against official sources), practical
next steps, and official government portals — always with the mandatory
awareness-not-advice disclaimer.

## Stack

| Concern | Choice |
|---|---|
| Framework | React 18 + Vite + TypeScript |
| Styling | Tailwind CSS (dark-first, glassmorphism) |
| Components | shadcn/ui (Radix primitives, copied in under `src/components/ui`) |
| Animation | Framer Motion (purposeful, reduced-motion aware) |
| 3D | React Three Fiber + drei — **landing hero only**, lazy-loaded |
| Data | TanStack Query |
| Routing | React Router |
| Icons | lucide-react |

## Architecture principles

- **No legal logic in the frontend.** Components under `src/components/legal/*`
  are pure renderers of the API response (see `src/types/contract.ts`, a typed
  mirror of the response contract). The UI never selects provisions, invents
  rationale, or computes thresholds.
- **The safe state is a real screen.** `legal_information_status ===
  "no_verified_provision_available"` renders `NoVerifiedProvisionState`, never an
  empty section.
- **Two reasoning layers stay separate.** `issue_match_reason` (Layer A) renders
  on the issue card; `provision_relevance_rationale` (Layer B) renders on each
  provision card — never merged.
- **The disclaimer always renders**, taken from the payload (not hardcoded).
- **The issue `similarity_score` is never shown to citizens** — only the
  human-readable `issue_match_reason`.
- **Privacy:** the scenario is sent only in the POST body; never persisted, never
  placed in a URL.
- **3D is decorative and guarded:** lazy-loaded, `aria-hidden`, capped DPR,
  paused offscreen, with a static fallback under `prefers-reduced-motion`.

## Backend integration

The frontend talks **only** to the Node.js gateway (`:5000`), never directly to
the FastAPI ML service.

| Call | Route | Notes |
|---|---|---|
| Analyze | `POST /api/analyze` `{ scenario }` | 20–2000 chars; returns the contract unchanged |
| Health | `GET /api/health` | optional service indicator |
| Domains | `GET /api/domains` | static domain list |

Status handling matches the gateway exactly:

- **200** → results (includes low-confidence — those are flags, not errors)
- **400** → input validation
- **429** → rate limited (10/min/IP)
- **503** → ML service unavailable (never a fabricated answer)

In development, Vite proxies `/api` → `http://localhost:5000` (override with
`VITE_GATEWAY_URL`). See `.env.example`.

## Scripts

```bash
npm install      # install dependencies
npm run dev      # dev server on http://localhost:3000 (proxies /api to :5000)
npm run build    # typecheck + production build to dist/
npm run preview  # preview the production build
npm run lint     # typecheck only (tsc --noEmit)
```

To run the full flow locally, start the ML service (`:8000`) and the gateway
(`:5000`) as described in the repo root, then `npm run dev` here.

## Structure

```
src/
├── main.tsx / App.tsx        entry + router
├── index.css                 design tokens (jade/brass palette), glass utilities
├── types/contract.ts         typed mirror of the API response contract
├── lib/                      cn() + gateway client
├── hooks/useAnalyze.ts       POST /analyze lifecycle (TanStack Query)
├── providers/                Theme (dark-first) + Query
├── components/
│   ├── ui/                   shadcn primitives
│   ├── brand/                LensMark + Logo (magnifying-glass wordmark)
│   ├── layout/               Navbar, Footer, RootLayout, PageTransition
│   ├── three/                HeroCanvas (guard) + HeroScene (R3F) + fallback
│   └── legal/                pure result renderers (domain, issue, provisions,
│                             steps, portals, safe state, disclaimer)
├── features/analyze/         ScenarioInput, AnalysisStages, ResultView, errors
└── pages/                    Landing, Analyze, HowItWorks, NotFound
```

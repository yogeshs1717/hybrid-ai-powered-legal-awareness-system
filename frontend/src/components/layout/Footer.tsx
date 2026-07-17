import { Link } from "react-router-dom";
import { Logo } from "@/components/brand/Logo";

export function Footer() {
  return (
    <footer className="mt-24 border-t border-white/10">
      <div className="container py-12">
        <div className="flex flex-col gap-10 md:flex-row md:items-start md:justify-between">
          <div className="max-w-sm">
            <Logo />
            <p className="mt-4 text-sm text-muted-foreground text-pretty">
              See the law more clearly. LegalLens helps Indian citizens understand
              which laws may relate to a real-life situation — in plain language.
            </p>
          </div>

          <nav className="grid grid-cols-2 gap-x-12 gap-y-2 text-sm sm:gap-x-20">
            <div className="flex flex-col gap-2">
              <span className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground/70">
                Product
              </span>
              <Link to="/" className="text-muted-foreground hover:text-foreground">
                Home
              </Link>
              <Link
                to="/how-it-works"
                className="text-muted-foreground hover:text-foreground"
              >
                How it works
              </Link>
              <Link
                to="/analyze"
                className="text-muted-foreground hover:text-foreground"
              >
                Analyze a situation
              </Link>
            </div>
            <div className="flex flex-col gap-2">
              <span className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground/70">
                About
              </span>
              <Link
                to="/how-it-works#scope"
                className="text-muted-foreground hover:text-foreground"
              >
                Scope &amp; limits
              </Link>
              <Link
                to="/how-it-works#trust"
                className="text-muted-foreground hover:text-foreground"
              >
                Trust &amp; safety
              </Link>
            </div>
          </nav>
        </div>

        <div className="mt-10 border-t border-white/10 pt-6">
          <p className="text-xs leading-relaxed text-muted-foreground/80 text-pretty">
            LegalLens provides legal <em>awareness</em>, not legal <em>advice</em>. It
            does not tell you whether a law definitely applies or whether you have a
            case. Always consult a qualified legal professional for advice specific to
            your situation.
          </p>
          <p className="mt-4 text-xs text-muted-foreground/60">
            © {new Date().getFullYear()} LegalLens · For legal awareness in India.
          </p>
        </div>
      </div>
    </footer>
  );
}

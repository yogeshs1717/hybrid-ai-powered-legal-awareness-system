import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Home, Compass, Scale, Moon, Sun, Menu, X, ArrowUpRight } from "lucide-react";
import { LensMark } from "@/components/brand/LensMark";
import { useTheme } from "@/providers/ThemeProvider";
import { LanguageDropdown } from "@/components/Translation";

const NAV = [
  { to: "/", label: "HOME", icon: Home },
  { to: "/how-it-works", label: "HOW IT WORKS", icon: Compass },
  { to: "/analyze", label: "ANALYZE", icon: Scale },
];

export function Navbar() {
  const { theme, toggleTheme } = useTheme();
  const [open, setOpen] = useState(false);
  const [time, setTime] = useState("");
  const location = useLocation();

  useEffect(() => setOpen(false), [location.pathname]);

  // Live digital clock in the canvas ruler (as in reference Image 2)
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-background/95 backdrop-blur-md border-b border-border select-none">
      {/* ---------- Main Studio Toolbar ---------- */}
      <div className="flex h-12 sm:h-14 items-center justify-between">
        {/* Left: Brand Icon Box */}
        <div className="flex items-center h-full">
          <Link
            to="/"
            aria-label="LegalLens home"
            className="flex items-center justify-center h-full px-4 border-r border-border hover:bg-muted/50 transition-colors"
          >
            <LensMark className="h-6 w-6 text-foreground" />
            <span className="ml-2 font-display font-bold text-sm tracking-tight hidden lg:inline">
              LegalLens
            </span>
          </Link>

          {/* Desktop Navigation Tabs */}
          <nav className="hidden md:flex h-full items-center">
            {NAV.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-1.5 h-full px-4 sm:px-5 text-xs font-mono font-bold tracking-wider border-r border-border transition-colors ${
                    isActive
                      ? "bg-[#00c5ff] text-black"
                      : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
                  }`
                }
              >
                <item.icon className="h-3.5 w-3.5" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Right: Actions, Language Dropdown & Theme Toggle */}
        <div className="flex items-center h-full px-3 sm:px-4 gap-2">
          {/* Language Selector Dropdown */}
          <LanguageDropdown />

          {/* Theme Toggle Button */}
          <button
            type="button"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
            className="h-9 w-9 flex items-center justify-center rounded-full border border-border hover:bg-muted/80 text-foreground transition-colors"
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>

          {/* High-Contrast Action Pill Button */}
          <Link
            to="/analyze"
            className="hidden sm:inline-flex items-center gap-1.5 h-9 px-4 rounded-full border-2 border-foreground bg-foreground text-background font-mono text-xs font-bold tracking-wider hover:bg-transparent hover:text-foreground transition-all duration-200"
          >
            <span>ANALYZE</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </Link>

          {/* Mobile Menu Toggle */}
          <button
            type="button"
            className="md:hidden h-9 w-9 flex items-center justify-center rounded-full border border-border hover:bg-muted text-foreground"
            onClick={() => setOpen((v) => !v)}
            aria-label={open ? "Close menu" : "Open menu"}
          >
            {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        </div>
      </div>

      {/* ---------- Canvas Coordinate Ruler (Like Reference Image 2) ---------- */}
      <div
        aria-hidden="true"
        className="w-full h-5 border-t border-border/60 bg-muted/20 flex items-center justify-between px-3 text-[9px] font-mono text-muted-foreground/60 overflow-hidden"
      >
        <div className="flex items-center gap-8 sm:gap-14 overflow-hidden">
          {[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300].map((tick) => (
            <span key={tick} className="flex items-center gap-1.5 shrink-0">
              <span className="inline-block w-px h-2 bg-border" />
              <span>{tick}</span>
            </span>
          ))}
        </div>
        {time && (
          <span className="font-mono text-[10px] text-muted-foreground font-semibold px-2 shrink-0 bg-background/80 rounded border border-border/40">
            {time}
          </span>
        )}
      </div>

      {/* ---------- Mobile Menu ---------- */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden md:hidden border-t border-border bg-background"
          >
            <div className="p-3 space-y-1">
              {NAV.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-mono font-bold uppercase transition-colors ${
                      isActive ? "bg-[#00c5ff] text-black" : "text-foreground hover:bg-muted"
                    }`
                  }
                >
                  <item.icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </NavLink>
              ))}
              <Link
                to="/analyze"
                className="flex items-center justify-center gap-2 mt-2 w-full py-2.5 rounded-lg bg-foreground text-background font-mono text-xs font-bold"
              >
                <span>ANALYZE A SITUATION</span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}

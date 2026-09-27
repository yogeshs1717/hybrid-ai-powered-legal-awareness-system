import { useEffect, useState, useRef, useCallback } from "react";
import { Globe, Check, ChevronDown, Loader2 } from "lucide-react";
import { useLocation } from "react-router-dom";

declare global {
  interface Window {
    google?: {
      translate?: {
        TranslateElement: new (
          options: {
            pageLanguage: string;
            includedLanguages: string;
            autoDisplay: boolean;
            layout?: number;
          },
          elementId: string
        ) => void;
      };
    };
    googleTranslateElementInit?: () => void;
  }
}

export type LangCode = "en" | "hi" | "kn";

export interface LanguageOption {
  code: LangCode;
  name: string;
  native: string;
}

export const LANGUAGES: LanguageOption[] = [
  { code: "en", name: "English", native: "English" },
  { code: "hi", name: "Hindi", native: "हिन्दी" },
  { code: "kn", name: "Kannada", native: "ಕನ್ನಡ" },
];

// In-memory cache for translated strings
const translationCache = new Map<string, string>();
// Maps any translated text back to its pristine English text
const toEnglishMap = new Map<string, string>();

/**
 * Remove all Google Translate cookies across all host variations and paths.
 */
function clearAllGoogleCookies() {
  const domain = window.location.hostname;
  const domainVariants = [
    "",
    domain,
    `.${domain}`,
    domain.replace(/^www\./, ""),
    `.${domain.replace(/^www\./, "")}`,
  ];
  const pathVariants = ["/", window.location.pathname];
  for (const d of domainVariants) {
    for (const p of pathVariants) {
      const dStr = d ? `; domain=${d}` : "";
      document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${p}${dStr}`;
      document.cookie = `googtrans=; max-age=0; path=${p}${dStr}`;
    }
  }
}

/**
 * Collect all visible text nodes in the DOM, skipping scripts, styles, SVGs,
 * and the translation component itself.
 */
function getTranslatableNodes(root: Node): { node: Text; text: string }[] {
  const results: { node: Text; text: string }[] = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent) return NodeFilter.FILTER_REJECT;
      const tag = parent.tagName.toLowerCase();
      if (
        tag === "script" ||
        tag === "style" ||
        tag === "noscript" ||
        tag === "svg" ||
        tag === "path" ||
        tag === "code" ||
        parent.closest("[data-no-translate]") ||
        parent.closest("[data-language-selector]")
      ) {
        return NodeFilter.FILTER_REJECT;
      }
      const val = node.nodeValue?.trim();
      if (!val || val.length < 2 || /^[\d\s.,:;!?()[\]{}<>\-_/\\|@#$%^&*+=~`'"]+$/.test(val)) {
        return NodeFilter.FILTER_REJECT;
      }
      return NodeFilter.FILTER_ACCEPT;
    },
  });

  let current: Node | null;
  while ((current = walker.nextNode())) {
    const textNode = current as Text;
    const text = textNode.nodeValue?.trim() || "";
    if (text) {
      results.push({ node: textNode, text });
    }
  }
  return results;
}

/**
 * Core Language Dropdown Component for the Navbar.
 */
export function LanguageDropdown({ className = "" }: { className?: string }) {
  const [currentLang, setCurrentLang] = useState<LangCode>("en");
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const currentLangRef = useRef<LangCode>("en");
  currentLangRef.current = currentLang;

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  // Translate all DOM text nodes to target language using backend /api/translate
  const translateDom = useCallback(async (target: LangCode) => {
    if (target === "en") return;

    const items = getTranslatableNodes(document.body);
    if (!items.length) return;

    // Collect unique strings that need translation
    const neededTexts: string[] = [];
    for (const item of items) {
      const cacheKey = `${target}:${item.text}`;
      if (translationCache.has(cacheKey)) {
        const translated = translationCache.get(cacheKey)!;
        const origFull = item.node.nodeValue || "";
        item.node.nodeValue = origFull.replace(item.text, translated);
      } else {
        if (!neededTexts.includes(item.text)) {
          neededTexts.push(item.text);
        }
      }
    }

    if (!neededTexts.length) return;

    // Batch translate in chunks of 30
    setIsLoading(true);
    try {
      const CHUNK_SIZE = 30;
      for (let i = 0; i < neededTexts.length; i += CHUNK_SIZE) {
        const chunk = neededTexts.slice(i, i + CHUNK_SIZE);
        const res = await fetch("/api/translate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ texts: chunk, target }),
        });

        if (res.ok) {
          const data = await res.json();
          const translations: string[] = data.translated || [];
          chunk.forEach((origText, idx) => {
            const translatedText = translations[idx] || origText;
            translationCache.set(`${target}:${origText}`, translatedText);

            // Keep reverse map pointing to true English
            const trueEnglish = toEnglishMap.get(origText.trim()) || origText.trim();
            toEnglishMap.set(translatedText.trim(), trueEnglish);
          });
        }
      }

      // Update remaining text nodes with cached translations
      for (const item of items) {
        const cacheKey = `${target}:${item.text}`;
        if (translationCache.has(cacheKey)) {
          const translated = translationCache.get(cacheKey)!;
          const origFull = item.node.nodeValue || "";
          item.node.nodeValue = origFull.replace(item.text, translated);
        }
      }
    } catch (err) {
      console.warn("DOM translation failed:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Handle language change
  const changeLanguage = useCallback(
    (lang: LangCode) => {
      setIsOpen(false);
      if (lang === currentLangRef.current) return;

      setCurrentLang(lang);
      localStorage.setItem("legallens_lang", lang);

      // Switching back to English:
      if (lang === "en") {
        clearAllGoogleCookies();

        // 1. In-place replacement back to English using reverse map
        let anyReverted = false;
        try {
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let curr: Node | null;
          while ((curr = walker.nextNode())) {
            const textNode = curr as Text;
            const fullVal = textNode.nodeValue || "";
            const trimmed = fullVal.trim();
            if (trimmed && toEnglishMap.has(trimmed)) {
              const englishText = toEnglishMap.get(trimmed)!;
              textNode.nodeValue = fullVal.replace(trimmed, englishText);
              anyReverted = true;
            }
          }
        } catch (_e) {
          // ignore
        }

        // 2. Try Google Translate built-in revert button if any
        try {
          const iframe = document.querySelector("iframe.goog-te-banner-frame") as HTMLIFrameElement | null;
          if (iframe && iframe.contentDocument) {
            const closeBtn = iframe.contentDocument.querySelector(".goog-close-link") as HTMLElement | null;
            if (closeBtn) closeBtn.click();
          }
          const ttClose = document.querySelector("#goog-gt-tt button, .goog-close-link") as HTMLElement | null;
          if (ttClose) ttClose.click();
        } catch (_e) {
          // ignore
        }

        // 3. If any Indic characters remain, reload to guarantee 100% clean English
        const stillHasIndic = /[\u0900-\u097F\u0C80-\u0CFF]/.test(document.body.innerText);
        if (stillHasIndic || !anyReverted) {
          window.location.reload();
          return;
        }

        return;
      }

      // Switching to Hindi or Kannada:
      const domain = window.location.hostname;
      document.cookie = `googtrans=/en/${lang}; path=/;`;
      document.cookie = `googtrans=/en/${lang}; path=/; domain=${domain};`;

      // Trigger Google Translate combo if present
      const combo = document.querySelector(".goog-te-combo") as HTMLSelectElement | null;
      if (combo) {
        combo.value = lang;
        combo.dispatchEvent(new Event("change", { bubbles: true }));
      }

      // Translate DOM in-place via backend /api/translate
      translateDom(lang);
    },
    [translateDom]
  );

  // Initialize and load saved language
  useEffect(() => {
    const saved = localStorage.getItem("legallens_lang") as LangCode | null;
    if (saved === "en") {
      setCurrentLang("en");
      clearAllGoogleCookies();
    } else if (saved === "hi" || saved === "kn") {
      setCurrentLang(saved);
      translateDom(saved);
    }

    // Set up Google Translate callback
    window.googleTranslateElementInit = () => {
      if (window.google?.translate?.TranslateElement) {
        new window.google.translate.TranslateElement(
          {
            pageLanguage: "en",
            includedLanguages: "en,hi,kn",
            autoDisplay: false,
          },
          "google_translate_element"
        );
      }
    };

    // Load Google Translate script safely
    const SCRIPT_ID = "google-translate-script";
    if (!document.getElementById(SCRIPT_ID)) {
      const script = document.createElement("script");
      script.id = SCRIPT_ID;
      script.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      script.async = true;
      document.body.appendChild(script);
    }
  }, [translateDom]);

  // Re-translate whenever the user navigates between routes
  useEffect(() => {
    if (currentLangRef.current !== "en") {
      const timer = setTimeout(() => {
        translateDom(currentLangRef.current);
      }, 150);
      return () => clearTimeout(timer);
    }
  }, [location.pathname, translateDom]);

  const activeOption = LANGUAGES.find((l) => l.code === currentLang) || LANGUAGES[0];

  return (
    <div
      ref={dropdownRef}
      data-no-translate="true"
      data-language-selector="true"
      className={`relative inline-block text-left ${className}`}
    >
      {/* Invisible container for Google Translate element */}
      <div
        id="google_translate_element"
        data-no-translate="true"
        style={{
          position: "fixed",
          top: "-9999px",
          left: "-9999px",
          width: "1px",
          height: "1px",
          overflow: "hidden",
          opacity: 0,
          pointerEvents: "none",
        }}
      />

      {/* Global CSS to clean up Google Translate widget UI */}
      <style>{`
        .goog-te-banner-frame.skiptranslate,
        iframe.goog-te-banner-frame,
        .goog-te-banner-frame {
          display: none !important;
          visibility: hidden !important;
          height: 0 !important;
        }
        body {
          top: 0px !important;
        }
        #goog-gt-tt,
        .goog-te-balloon-frame,
        .goog-tooltip,
        .goog-tooltip:hover {
          display: none !important;
        }
        .goog-text-highlight {
          background-color: transparent !important;
          box-shadow: none !important;
        }
        .skiptranslate > iframe {
          display: none !important;
        }
      `}</style>

      {/* Language Trigger Button in Navbar */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        className="inline-flex items-center gap-1.5 h-9 px-3 rounded-full border border-border bg-card/60 hover:bg-muted/80 text-xs font-medium text-foreground transition-all duration-200 select-none cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
      >
        {isLoading ? (
          <Loader2 className="w-3.5 h-3.5 animate-spin text-primary" />
        ) : (
          <Globe className="w-3.5 h-3.5 text-primary" />
        )}
        <span>{activeOption.native}</span>
        <ChevronDown
          className={`w-3 h-3 text-muted-foreground transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {/* Dropdown Menu (opens downward directly beneath the button) */}
      {isOpen && (
        <div
          role="listbox"
          aria-label="Select Language"
          className="absolute top-full mt-2 right-0 w-36 rounded-xl border border-border bg-card shadow-xl backdrop-blur-xl p-1 z-50 animate-in fade-in zoom-in-95 duration-100"
        >
          <div className="space-y-0.5">
            {LANGUAGES.map((lang) => {
              const isSelected = lang.code === currentLang;
              return (
                <button
                  key={lang.code}
                  role="option"
                  aria-selected={isSelected}
                  type="button"
                  onClick={() => changeLanguage(lang.code)}
                  className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isSelected
                      ? "bg-primary text-primary-foreground font-semibold"
                      : "text-foreground hover:bg-muted"
                  }`}
                >
                  <span>{lang.native}</span>
                  {isSelected && <Check className="w-3.5 h-3.5 stroke-[2.5]" />}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// Export default Translation component for backward compatibility in App.tsx
export function Translation() {
  return null;
}

import { useEffect, useState, useRef, useCallback } from "react";
import { Globe, Check, Loader2, Sparkles } from "lucide-react";
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

type LangCode = "en" | "hi" | "kn";

interface LanguageOption {
  code: LangCode;
  name: string;
  native: string;
}

const LANGUAGES: LanguageOption[] = [
  { code: "en", name: "English", native: "English" },
  { code: "hi", name: "Hindi", native: "हिन्दी" },
  { code: "kn", name: "Kannada", native: "ಕನ್ನಡ" },
];

// In-memory cache for translated strings to avoid redundant API roundtrips
const translationCache = new Map<string, string>();
// Maps any translated text (Hindi / Kannada) back to its original English text
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
        parent.closest("aside[aria-label='Language Selector']")
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

export function Translation() {
  const [currentLang, setCurrentLang] = useState<LangCode>("en");
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();
  const currentLangRef = useRef<LangCode>("en");
  currentLangRef.current = currentLang;

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

    // Batch translate uncached strings in chunks of 30
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
          // ignore walker error
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

        // 3. Verify if any Indic characters (Devanagari \u0900-\u097F or Kannada \u0C80-\u0CFF) remain.
        // If anything is still not English or in-place didn't match, reload to guarantee 100% original English
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

  // Initialize and load saved language or Google Translate
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

  return (
    <>
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

      {/* Floating Modern Language Selector Bar — bottom-right with maximum z-index */}
      <aside
        aria-label="Language Selector"
        data-no-translate="true"
        className="fixed bottom-5 right-5 z-[99999] pointer-events-auto select-none"
        style={{ zIndex: 99999 }}
      >
        <div className="flex items-center gap-1.5 p-1.5 rounded-full border border-white/20 bg-slate-950/90 shadow-2xl backdrop-blur-xl ring-1 ring-white/10">
          {/* Label / Icon */}
          <div className="flex items-center gap-1.5 pl-2.5 pr-2 py-1 text-slate-300 font-medium text-xs border-r border-white/10">
            <Globe className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span className="hidden sm:inline text-[11px] text-slate-400">Language:</span>
          </div>

          {/* Language Buttons */}
          <div className="flex items-center gap-1">
            {LANGUAGES.map((lang) => {
              const isSelected = lang.code === currentLang;
              return (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => changeLanguage(lang.code)}
                  className={`cursor-pointer flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold transition-all duration-200 active:scale-95 ${
                    isSelected
                      ? "bg-emerald-500 text-slate-950 shadow-md scale-105"
                      : "text-slate-300 hover:text-white hover:bg-white/10"
                  }`}
                  aria-pressed={isSelected}
                  title={`Translate whole app to ${lang.name}`}
                >
                  {isSelected && !isLoading && <Check className="w-3 h-3 stroke-[3]" />}
                  {isSelected && isLoading && <Loader2 className="w-3 h-3 animate-spin" />}
                  <span>{lang.native}</span>
                </button>
              );
            })}
          </div>

          {/* Status Indicator */}
          {currentLang !== "en" && !isLoading && (
            <div className="hidden md:flex items-center gap-1 pr-2 pl-1 text-[10px] text-emerald-400/80 font-medium">
              <Sparkles className="w-3 h-3" />
              <span>Translated</span>
            </div>
          )}
          {isLoading && (
            <div className="hidden md:flex items-center gap-1 pr-2 pl-1 text-[10px] text-amber-400 font-medium animate-pulse">
              <span>Translating...</span>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}

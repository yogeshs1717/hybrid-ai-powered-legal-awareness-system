"use strict";

// In-memory cache for translations (max 2000 entries)
const translationCache = new Map();
const MAX_CACHE_SIZE = 2000;

function getCacheKey(text, targetLang, sourceLang) {
  return `${sourceLang || "auto"}:${targetLang}:${text}`;
}

function setCache(key, val) {
  if (translationCache.size >= MAX_CACHE_SIZE) {
    // Delete oldest entry
    const firstKey = translationCache.keys().next().value;
    translationCache.delete(firstKey);
  }
  translationCache.set(key, val);
}

/**
 * Detect script based on unicode range.
 * Supports Devanagari (Hindi) and Kannada script.
 */
function detectScript(text) {
  if (typeof text !== "string") return "en";
  if (/[\u0C80-\u0CFF]/.test(text)) {
    return "kn"; // Kannada
  }
  if (/[\u0900-\u097F]/.test(text)) {
    return "hi"; // Hindi (Devanagari)
  }
  return "en";
}

/**
 * Translate a single text string using resilient multi-provider translation.
 * Uses primary Google Chrome-extension endpoint with automatic fallback to
 * Android Translate endpoint and MyMemory Translation API.
 * Gracefully falls back to the original text on any total network failure or timeout.
 */
async function translateText(text, targetLang = "en", sourceLang = "auto") {
  if (!text || typeof text !== "string") return text;
  const trimmed = text.trim();
  if (!trimmed) return text;

  // Don't translate if target is the same as source
  if (sourceLang === targetLang && targetLang !== "auto") {
    return text;
  }

  const key = getCacheKey(trimmed, targetLang, sourceLang);
  if (translationCache.has(key)) {
    return translationCache.get(key);
  }

  const encodedQuery = encodeURIComponent(trimmed);
  const sl = encodeURIComponent(sourceLang || "auto");
  const tl = encodeURIComponent(targetLang);

  // --- Provider 1: Google Chrome-Extension API (High throughput, no 429 captcha) ---
  try {
    const url = `https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=${sl}&tl=${tl}&q=${encodedQuery}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4500);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
      },
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      let result = null;
      if (Array.isArray(data)) {
        if (typeof data[0] === "string") {
          result = data[0];
        } else if (Array.isArray(data[0]) && typeof data[0][0] === "string") {
          result = data[0][0];
        }
      }
      if (result && result.trim()) {
        setCache(key, result.trim());
        return result.trim();
      }
    }
  } catch (_err) {
    // Fall through to next provider
  }

  // --- Provider 2: Google Android Translate API ---
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=at&sl=${sl}&tl=${tl}&dt=t&q=${encodedQuery}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "User-Agent": "GoogleTranslate/6.28.0.05.421483610 (Linux; U; Android 12)",
      },
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      if (Array.isArray(data) && Array.isArray(data[0])) {
        const translated = data[0]
          .map((chunk) => (Array.isArray(chunk) && chunk[0] ? chunk[0] : ""))
          .join("");
        if (translated && translated.trim()) {
          setCache(key, translated.trim());
          return translated.trim();
        }
      }
    }
  } catch (_err) {
    // Fall through to next provider
  }

  // --- Provider 3: MyMemory Translation API ---
  try {
    const src = sourceLang === "auto" ? "" : sourceLang;
    const pair = src ? `${src}|${targetLang}` : targetLang;
    const url = `https://api.mymemory.translated.net/get?q=${encodedQuery}&langpair=${encodeURIComponent(pair)}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);

    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (response.ok) {
      const data = await response.json();
      const translated = data?.responseData?.translatedText;
      if (translated && translated.trim() && !translated.startsWith("MYMEMORY WARNING")) {
        setCache(key, translated.trim());
        return translated.trim();
      }
    }
  } catch (_err) {
    // Final fallback
  }

  return text;
}

/**
 * Translate an array of text strings.
 */
async function translateArray(texts, targetLang = "en", sourceLang = "auto") {
  if (!Array.isArray(texts)) return texts;
  return Promise.all(
    texts.map((item) =>
      typeof item === "string"
        ? translateText(item, targetLang, sourceLang)
        : Promise.resolve(item)
    )
  );
}

module.exports = {
  detectScript,
  translateText,
  translateArray,
  translationCache,
};

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
 * Translate a single text string using Google Translate endpoint.
 * Gracefully falls back to the original text on any network failure or timeout.
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

  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${encodeURIComponent(
      sourceLang
    )}&tl=${encodeURIComponent(targetLang)}&dt=t&q=${encodeURIComponent(trimmed)}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      },
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      return text;
    }

    const data = await response.json();
    if (Array.isArray(data) && Array.isArray(data[0])) {
      const translated = data[0]
        .map((chunk) => (Array.isArray(chunk) && chunk[0] ? chunk[0] : ""))
        .join("");
      if (translated) {
        setCache(key, translated);
        return translated;
      }
    }
  } catch (err) {
    // Return original on any fetch error or abort
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

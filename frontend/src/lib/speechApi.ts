/**
 * Speech Service API Client.
 *
 * Communicates with the local Whisper-powered Speech Service (port 8001 or Vite /speech proxy).
 * Transcribes English, Hindi, and Kannada speech recordings.
 */

export interface TranscribeResult {
  transcript: string;
  language: string; // "en" | "hi" | "kn" or other ISO code
  language_probability: number;
  duration?: number;
}

export interface SpeechHealthResult {
  status: string;
  service: string;
  model_size: string;
  device: string;
  compute_type: string;
  model_loaded: boolean;
  supported_languages: string[];
}

export class SpeechApiError extends Error {
  status?: number;
  code: string;

  constructor(message: string, code = "speech_error", status?: number) {
    super(message);
    this.name = "SpeechApiError";
    this.code = code;
    this.status = status;
  }
}

// In development, Vite proxies /speech to http://localhost:8001
// Can also be overridden with VITE_SPEECH_API_URL
const SPEECH_BASE = import.meta.env.VITE_SPEECH_API_URL ?? "/speech";

/**
 * Checks if the speech service is reachable and the model is loaded.
 */
export async function checkSpeechHealth(signal?: AbortSignal): Promise<SpeechHealthResult> {
  try {
    const res = await fetch(`${SPEECH_BASE}/health`, {
      method: "GET",
      signal,
    });
    if (!res.ok) {
      throw new SpeechApiError("Speech service is reporting degraded status", "service_degraded", res.status);
    }
    return (await res.json()) as SpeechHealthResult;
  } catch (err: unknown) {
    if (err instanceof SpeechApiError) throw err;
    const msg = (err as Error)?.message || "Speech service is not reachable.";
    throw new SpeechApiError(
      `Could not connect to Speech Service at ${SPEECH_BASE}. Ensure speech-service is running on port 8001. (${msg})`,
      "network_error",
    );
  }
}

/**
 * Uploads an audio blob to /transcribe and returns the transcription with detected language.
 */
export async function transcribeAudio(
  audioBlob: Blob,
  options?: {
    language?: string;
    signal?: AbortSignal;
  },
): Promise<TranscribeResult> {
  if (!audioBlob || audioBlob.size === 0) {
    throw new SpeechApiError("Recording was empty. Please speak your complaint and try again.", "empty_recording", 400);
  }

  // Determine file extension from MIME type
  let filename = "recording.webm";
  const type = audioBlob.type.toLowerCase();
  if (type.includes("wav")) {
    filename = "recording.wav";
  } else if (type.includes("ogg")) {
    filename = "recording.ogg";
  } else if (type.includes("mp4") || type.includes("m4a")) {
    filename = "recording.m4a";
  }

  const formData = new FormData();
  formData.append("file", audioBlob, filename);
  if (options?.language && options.language !== "auto") {
    formData.append("language", options.language);
  }

  const controller = new AbortController();
  const timeoutMs = 60000; // 60s timeout for local CPU Whisper transcription
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  if (options?.signal) {
    options.signal.addEventListener("abort", () => controller.abort());
  }

  try {
    const response = await fetch(`${SPEECH_BASE}/transcribe`, {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      return (await response.json()) as TranscribeResult;
    }

    let detail = "";
    try {
      const errJson = await response.json();
      detail = errJson.detail || errJson.error || "";
    } catch {
      // Non-JSON response
    }

    if (response.status === 400) {
      throw new SpeechApiError(
        detail || "Invalid audio recording. Please try speaking again.",
        "invalid_audio",
        400,
      );
    } else if (response.status === 413) {
      throw new SpeechApiError(
        detail || "Audio recording is too long. Please record a shorter message.",
        "file_too_large",
        413,
      );
    } else if (response.status === 503) {
      throw new SpeechApiError(
        detail || "Whisper speech model is still loading or unavailable. Please wait a moment and try again.",
        "model_unavailable",
        503,
      );
    } else {
      throw new SpeechApiError(
        detail || `Transcription failed with status ${response.status}.`,
        "server_error",
        response.status,
      );
    }
  } catch (err: unknown) {
    clearTimeout(timeoutId);
    if (err instanceof SpeechApiError) throw err;
    if ((err as Error)?.name === "AbortError") {
      throw new SpeechApiError(
        "Transcription timed out. The local speech model is taking longer than expected.",
        "timeout",
        504,
      );
    }
    throw new SpeechApiError(
      `Cannot reach Speech Service at ${SPEECH_BASE}. Ensure the speech service is running on port 8001.`,
      "network_error",
    );
  }
}

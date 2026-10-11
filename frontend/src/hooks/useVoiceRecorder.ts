import { useState, useRef, useCallback, useEffect } from "react";
import { transcribeAudio, TranscribeResult, SpeechApiError } from "@/lib/speechApi";

export interface VoiceRecorderState {
  isRecording: boolean;
  isTranscribing: boolean;
  recordingSeconds: number;
  detectedLanguage: {
    code: string;
    label: string;
    confidence: number;
  } | null;
  error: {
    title: string;
    message: string;
  } | null;
}

export interface UseVoiceRecorderOptions {
  onTranscriptionSuccess?: (result: TranscribeResult) => void;
  languageHint?: string; // "en" | "hi" | "kn" | "auto"
}

export function getLanguageLabel(code: string): string {
  switch (code.toLowerCase()) {
    case "hi":
      return "हिन्दी (Hindi)";
    case "kn":
      return "ಕನ್ನಡ (Kannada)";
    case "en":
      return "English";
    default:
      return code.toUpperCase();
  }
}

export function useVoiceRecorder(options?: UseVoiceRecorderOptions) {
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [detectedLanguage, setDetectedLanguage] = useState<VoiceRecorderState["detectedLanguage"]>(null);
  const [error, setError] = useState<VoiceRecorderState["error"]>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioStreamRef = useRef<MediaStream | null>(null);
  const timerIntervalRef = useRef<number | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Cleanup helper to guarantee all tracks in the media stream are stopped
  const stopAllTracks = useCallback(() => {
    if (audioStreamRef.current) {
      audioStreamRef.current.getTracks().forEach((track) => {
        try {
          track.stop();
        } catch {
          // ignore
        }
      });
      audioStreamRef.current = null;
    }
  }, []);

  const clearTimer = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearTimer();
      stopAllTracks();
    };
  }, [clearTimer, stopAllTracks]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const startRecording = useCallback(async () => {
    clearError();
    setDetectedLanguage(null);

    // 1. Check browser mediaDevices support
    if (
      typeof navigator === "undefined" ||
      !navigator.mediaDevices ||
      typeof navigator.mediaDevices.getUserMedia !== "function"
    ) {
      setError({
        title: "Microphone Not Supported",
        message: "Your current browser does not support audio recording. Please use modern Chrome, Firefox, or Edge.",
      });
      return;
    }

    try {
      // 2. Request microphone permission
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      audioStreamRef.current = stream;

      // 3. Find optimal supported MIME type
      let mimeType = "";
      if (typeof MediaRecorder !== "undefined" && typeof MediaRecorder.isTypeSupported === "function") {
        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
          mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
          mimeType = "audio/webm";
        } else if (MediaRecorder.isTypeSupported("audio/ogg;codecs=opus")) {
          mimeType = "audio/ogg;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/mp4")) {
          mimeType = "audio/mp4";
        }
      }

      const recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        // Collect recorded chunks into a single Blob
        const recordedBlob = new Blob(audioChunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });
        audioChunksRef.current = [];

        // Stop all hardware tracks immediately
        stopAllTracks();

        if (recordedBlob.size === 0) {
          setError({
            title: "Empty Recording",
            message: "No audio was captured. Please speak into your microphone and try again.",
          });
          setIsRecording(false);
          return;
        }

        // Send to Speech Service for transcription
        setIsTranscribing(true);
        try {
          const result = await transcribeAudio(recordedBlob, {
            language: options?.languageHint,
          });

          const langCode = result.language;
          const langConfidence = Math.round(result.language_probability * 100);
          setDetectedLanguage({
            code: langCode,
            label: getLanguageLabel(langCode),
            confidence: langConfidence,
          });

          if (!result.transcript || result.transcript.trim().length === 0) {
            setError({
              title: "No Speech Detected",
              message: "We couldn't hear any clear speech. Please speak closer to your microphone and try again.",
            });
          } else {
            options?.onTranscriptionSuccess?.(result);
          }
        } catch (err: unknown) {
          const speechErr = err as SpeechApiError;
          setError({
            title: "Transcription Failed",
            message: speechErr.message || "Could not transcribe audio. Please check speech service status.",
          });
        } finally {
          setIsTranscribing(false);
          setIsRecording(false);
        }
      };

      // Start recording with timeslice (chunk every 250ms)
      recorder.start(250);
      setIsRecording(true);
      setRecordingSeconds(0);

      // Start duration counter
      clearTimer();
      timerIntervalRef.current = window.setInterval(() => {
        setRecordingSeconds((prev) => prev + 1);
      }, 1000);
    } catch (err: unknown) {
      stopAllTracks();
      clearTimer();
      setIsRecording(false);

      const errName = (err as Error)?.name || "";
      if (errName === "NotAllowedError" || errName === "PermissionDeniedError") {
        setError({
          title: "Microphone Access Denied",
          message: "Permission to use your microphone was blocked. Please enable microphone access in your browser site permissions.",
        });
      } else if (errName === "NotFoundError" || errName === "DevicesNotFoundError") {
        setError({
          title: "Microphone Not Found",
          message: "No audio input device was found on your system. Please plug in a microphone.",
        });
      } else {
        setError({
          title: "Microphone Error",
          message: (err as Error)?.message || "Could not access audio recording on your device.",
        });
      }
    }
  }, [clearError, clearTimer, stopAllTracks, options]);

  const stopRecording = useCallback(() => {
    clearTimer();
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      try {
        mediaRecorderRef.current.stop();
      } catch {
        // ignore
      }
    }
  }, [clearTimer]);

  const cancelRecording = useCallback(() => {
    clearTimer();
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      try {
        // Remove onstop handler so we don't trigger transcription
        mediaRecorderRef.current.onstop = null;
        mediaRecorderRef.current.stop();
      } catch {
        // ignore
      }
    }
    stopAllTracks();
    audioChunksRef.current = [];
    setIsRecording(false);
    setRecordingSeconds(0);
  }, [clearTimer, stopAllTracks]);

  return {
    isRecording,
    isTranscribing,
    recordingSeconds,
    detectedLanguage,
    error,
    clearError,
    startRecording,
    stopRecording,
    cancelRecording,
  };
}

import { useState, useRef, useCallback, useEffect } from "react";
import { transcribeAudio, TranscribeResult, SpeechApiError } from "@/lib/speechApi";

export interface VoiceRecorderState {
  isRecording: boolean;
  isTranscribing: boolean;
  recordingSeconds: number;
  audioLevel: number; // 0 to 100 representing microphone input volume
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

/**
 * Finds the best supported audio MIME type across modern browsers (Chrome, Firefox, Safari, Edge).
 */
function getOptimalAudioMimeType(): string {
  if (typeof MediaRecorder === "undefined" || typeof MediaRecorder.isTypeSupported !== "function") {
    return "";
  }
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/ogg;codecs=opus",
    "audio/ogg",
    "audio/mp4",
    "audio/wav",
  ];
  for (const candidate of candidates) {
    if (MediaRecorder.isTypeSupported(candidate)) {
      return candidate;
    }
  }
  return "";
}

export function useVoiceRecorder(options?: UseVoiceRecorderOptions) {
  const optionsRef = useRef(options);
  optionsRef.current = options;

  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [audioLevel, setAudioLevel] = useState(0);
  const [detectedLanguage, setDetectedLanguage] = useState<VoiceRecorderState["detectedLanguage"]>(null);
  const [error, setError] = useState<VoiceRecorderState["error"]>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioStreamRef = useRef<MediaStream | null>(null);
  const timerIntervalRef = useRef<number | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Web Audio API resources for live audio metering / visualizer
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animFrameIdRef = useRef<number | null>(null);

  const clearTimer = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = null;
    }
  }, []);

  // Cleanup helper to guarantee all tracks in the media stream and audio context are closed
  const stopAllAudioResources = useCallback(() => {
    if (animFrameIdRef.current) {
      cancelAnimationFrame(animFrameIdRef.current);
      animFrameIdRef.current = null;
    }
    setAudioLevel(0);

    if (audioContextRef.current) {
      try {
        if (audioContextRef.current.state !== "closed") {
          audioContextRef.current.close().catch(() => {});
        }
      } catch {
        // ignore
      }
      audioContextRef.current = null;
    }
    analyserRef.current = null;

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

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearTimer();
      stopAllAudioResources();
    };
  }, [clearTimer, stopAllAudioResources]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const startRecording = useCallback(async () => {
    clearError();
    setDetectedLanguage(null);
    setAudioLevel(0);

    // 1. Check browser mediaDevices support
    if (
      typeof navigator === "undefined" ||
      !navigator.mediaDevices ||
      typeof navigator.mediaDevices.getUserMedia !== "function"
    ) {
      setError({
        title: "Microphone Not Supported",
        message: "Your browser does not support audio recording. Please use modern Chrome, Firefox, Edge, or Brave.",
      });
      return;
    }

    try {
      // 2. Request microphone permission with fallback to unconstrained audio
      let stream: MediaStream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            channelCount: 1,
            sampleRate: 16000,
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
        });
      } catch {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      }

      audioStreamRef.current = stream;

      // 3. Setup Web Audio Analyser for live visual audio metering
      try {
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (AudioCtx) {
          const audioCtx = new AudioCtx();
          if (audioCtx.state === "suspended") {
            audioCtx.resume().catch(() => {});
          }
          const analyser = audioCtx.createAnalyser();
          analyser.fftSize = 256;
          analyser.smoothingTimeConstant = 0.5;

          const source = audioCtx.createMediaStreamSource(stream);
          source.connect(analyser);

          audioContextRef.current = audioCtx;
          analyserRef.current = analyser;

          const dataArray = new Uint8Array(analyser.frequencyBinCount);
          const updateLevel = () => {
            if (!analyserRef.current) return;
            analyserRef.current.getByteFrequencyData(dataArray);
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
              sum += dataArray[i];
            }
            const average = sum / dataArray.length;
            // Scale and clamp between 0 and 100
            const level = Math.min(100, Math.round((average / 128) * 100));
            setAudioLevel(level);
            animFrameIdRef.current = requestAnimationFrame(updateLevel);
          };
          animFrameIdRef.current = requestAnimationFrame(updateLevel);
        }
      } catch {
        // Audio metering is a progressive enhancement; recording proceeds even if AudioContext fails
      }

      // 4. Determine best MIME type and instantiate MediaRecorder
      const mimeType = getOptimalAudioMimeType();
      const recorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        // Collect recorded chunks into a single Blob
        const recordedType = recorder.mimeType || mimeType || "audio/webm";
        const recordedBlob = new Blob(audioChunksRef.current, { type: recordedType });
        audioChunksRef.current = [];

        // Stop all hardware tracks and metering immediately
        stopAllAudioResources();

        if (recordedBlob.size === 0) {
          setError({
            title: "Empty Recording",
            message: "No audio was captured. Please check that your microphone is unmuted and speak clearly.",
          });
          setIsRecording(false);
          setIsTranscribing(false);
          return;
        }

        // Send to Speech Service for transcription
        setIsTranscribing(true);
        try {
          const result = await transcribeAudio(recordedBlob, {
            language: optionsRef.current?.languageHint,
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
              message: "We couldn't hear any clear words. Please speak closer to your microphone and try again.",
            });
          } else {
            optionsRef.current?.onTranscriptionSuccess?.(result);
          }
        } catch (err: unknown) {
          const speechErr = err as SpeechApiError;
          setError({
            title: "Transcription Failed",
            message: speechErr.message || "Could not transcribe audio. Ensure the Speech Service is running on port 8001.",
          });
        } finally {
          setIsTranscribing(false);
          setIsRecording(false);
        }
      };

      // Start recording with timeslice (chunk every 200ms)
      recorder.start(200);
      setIsRecording(true);
      setRecordingSeconds(0);

      // Start duration counter
      clearTimer();
      timerIntervalRef.current = window.setInterval(() => {
        setRecordingSeconds((prev) => prev + 1);
      }, 1000);
    } catch (err: unknown) {
      stopAllAudioResources();
      clearTimer();
      setIsRecording(false);

      const errName = (err as Error)?.name || "";
      if (errName === "NotAllowedError" || errName === "PermissionDeniedError") {
        setError({
          title: "Microphone Access Denied",
          message: "Permission to use your microphone was blocked. Please enable microphone permissions in your browser site settings.",
        });
      } else if (errName === "NotFoundError" || errName === "DevicesNotFoundError") {
        setError({
          title: "Microphone Not Found",
          message: "No audio input device was found on your system. Please plug in or select a working microphone.",
        });
      } else {
        setError({
          title: "Microphone Error",
          message: (err as Error)?.message || "Could not access audio recording on your device.",
        });
      }
    }
  }, [clearError, clearTimer, stopAllAudioResources]);

  const stopRecording = useCallback(() => {
    clearTimer();
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      try {
        // Flush any remaining audio data before stopping
        if (typeof recorder.requestData === "function") {
          recorder.requestData();
        }
        recorder.stop();
      } catch (err) {
        console.warn("Error stopping MediaRecorder:", err);
      }
    }
  }, [clearTimer]);

  const cancelRecording = useCallback(() => {
    clearTimer();
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      try {
        // Nullify onstop handler so cancellation does not trigger transcription
        recorder.onstop = null;
        recorder.stop();
      } catch {
        // ignore
      }
    }
    stopAllAudioResources();
    audioChunksRef.current = [];
    setIsRecording(false);
    setRecordingSeconds(0);
  }, [clearTimer, stopAllAudioResources]);

  return {
    isRecording,
    isTranscribing,
    recordingSeconds,
    audioLevel,
    detectedLanguage,
    error,
    clearError,
    startRecording,
    stopRecording,
    cancelRecording,
  };
}

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Mic,
  Square,
  Loader2,
  AlertCircle,
  X,
  Volume2,
  CheckCircle2,
  Languages,
} from "lucide-react";
import { useVoiceRecorder, VoiceRecorderState, getLanguageLabel } from "@/hooks/useVoiceRecorder";
import { TranscribeResult } from "@/lib/speechApi";
import { cn } from "@/lib/utils";

interface VoiceRecorderPanelProps {
  onTranscriptReceived: (transcript: string, languageInfo: VoiceRecorderState["detectedLanguage"]) => void;
  disabled?: boolean;
}

type LangOption = "auto" | "en" | "hi" | "kn";

const LANGUAGE_OPTIONS: { id: LangOption; label: string; sub: string }[] = [
  { id: "auto", label: "Auto", sub: "Detect" },
  { id: "en", label: "English", sub: "EN" },
  { id: "hi", label: "हिन्दी", sub: "Hindi" },
  { id: "kn", label: "ಕನ್ನಡ", sub: "Kannada" },
];

export function VoiceRecorderPanel({
  onTranscriptReceived,
  disabled = false,
}: VoiceRecorderPanelProps) {
  // Initialize language selection from localStorage if user chose Hindi or Kannada in the app header
  const [selectedLang, setSelectedLang] = useState<LangOption>(() => {
    try {
      const saved = localStorage.getItem("legallens_lang");
      if (saved === "kn" || saved === "hi" || saved === "en") return saved as LangOption;
    } catch {
      // ignore
    }
    return "auto";
  });

  const {
    isRecording,
    isTranscribing,
    recordingSeconds,
    detectedLanguage,
    error,
    clearError,
    startRecording,
    stopRecording,
    cancelRecording,
  } = useVoiceRecorder({
    languageHint: selectedLang === "auto" ? undefined : selectedLang,
    onTranscriptionSuccess: (result: TranscribeResult) => {
      onTranscriptReceived(result.transcript, {
        code: result.language,
        label: getLanguageLabel(result.language),
        confidence: Math.round(result.language_probability * 100),
      });
    },
  });

  // Sync if app language changes in localStorage
  useEffect(() => {
    const handleStorage = () => {
      const saved = localStorage.getItem("legallens_lang");
      if (saved === "kn" || saved === "hi" || saved === "en") {
        setSelectedLang(saved as LangOption);
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const getActiveLangName = () => {
    switch (selectedLang) {
      case "kn":
        return "ಕನ್ನಡ (Kannada)";
      case "hi":
        return "हिन्दी (Hindi)";
      case "en":
        return "English";
      default:
        return "Auto-Detect";
    }
  };

  return (
    <div className="w-full mb-3 select-none">
      {/* Recording / In-Progress Ribbon */}
      <AnimatePresence mode="wait">
        {isRecording && (
          <motion.div
            key="recording-state"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="rounded-lg border-2 border-red-500/50 bg-red-500/10 p-3 sm:p-4 mb-3 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-sm"
          >
            <div className="flex items-center gap-3">
              <span className="relative flex h-3.5 w-3.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75" />
                <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-red-600" />
              </span>

              <div className="flex flex-col">
                <span className="font-mono text-xs font-bold text-red-600 dark:text-red-400 uppercase tracking-wide flex items-center gap-1.5">
                  <Volume2 className="h-3.5 w-3.5 animate-pulse" />
                  Recording Audio ({formatTime(recordingSeconds)}) • {getActiveLangName()}
                </span>
                <span className="text-[11px] text-muted-foreground font-mono">
                  Speak clearly into your microphone... Whisper will transcribe your voice.
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
              <button
                type="button"
                onClick={stopRecording}
                className="inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-md bg-red-600 hover:bg-red-700 text-white font-mono text-xs font-bold uppercase shadow transition-all active:scale-95 cursor-pointer"
              >
                <Square className="h-3 w-3 fill-current" />
                <span>Done Recording</span>
              </button>

              <button
                type="button"
                onClick={cancelRecording}
                className="inline-flex items-center justify-center gap-1 px-2.5 py-1.5 rounded-md border border-border hover:bg-muted font-mono text-xs text-muted-foreground hover:text-foreground transition-all cursor-pointer"
                title="Cancel recording"
              >
                <X className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Cancel</span>
              </button>
            </div>
          </motion.div>
        )}

        {isTranscribing && (
          <motion.div
            key="transcribing-state"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="rounded-lg border-2 border-[#00c5ff]/40 bg-[#00c5ff]/10 p-3 sm:p-4 mb-3 flex items-center gap-3"
          >
            <Loader2 className="h-4 w-4 animate-spin text-[#00c5ff] shrink-0" />
            <div className="flex flex-col">
              <span className="font-mono text-xs font-bold text-[#0099cc] dark:text-[#00c5ff] uppercase tracking-wide">
                Transcribing Speech via Whisper AI ({getActiveLangName()})…
              </span>
              <span className="text-[11px] text-muted-foreground font-mono">
                Processing locally on CPU with int8 quantization. No external API calls.
              </span>
            </div>
          </motion.div>
        )}

        {error && (
          <motion.div
            key="error-state"
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            className="rounded-lg border border-destructive/40 bg-destructive/10 p-3 mb-3 flex items-start justify-between gap-3 text-xs"
          >
            <div className="flex items-start gap-2">
              <AlertCircle className="h-4 w-4 text-destructive shrink-0 mt-0.5" />
              <div>
                <strong className="font-bold text-destructive font-mono block">
                  {error.title}
                </strong>
                <span className="text-muted-foreground leading-relaxed">
                  {error.message}
                </span>
              </div>
            </div>
            <button
              type="button"
              onClick={clearError}
              className="text-muted-foreground hover:text-foreground p-0.5 cursor-pointer"
            >
              <X className="h-4 w-4" />
            </button>
          </motion.div>
        )}

        {detectedLanguage && !isRecording && !isTranscribing && (
          <motion.div
            key="success-banner"
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3.5 py-2 mb-3 flex flex-wrap items-center justify-between gap-2"
          >
            <div className="flex items-center gap-2 text-xs">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span className="font-mono font-bold text-emerald-700 dark:text-emerald-300">
                Transcribed in {detectedLanguage.label}
              </span>
              <span className="font-mono text-[10px] text-muted-foreground">
                ({detectedLanguage.confidence}% confidence)
              </span>
            </div>
            <span className="text-[11px] text-muted-foreground font-mono">
              Transcript inserted below. Review and edit before submitting.
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Microphone & Language Bar (Shown when idle) */}
      {!isRecording && !isTranscribing && (
        <div className="flex flex-wrap items-center justify-between gap-2 pb-1 bg-muted/30 p-2 rounded-lg border border-border/60">
          <div className="flex items-center gap-2">
            <button
              type="button"
              disabled={disabled}
              onClick={startRecording}
              className={cn(
                "inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md border border-red-500/30 bg-red-500/10 hover:bg-red-500/20 text-foreground font-mono text-xs font-semibold transition-all shadow-2xs hover:border-red-500/60 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer",
              )}
            >
              <Mic className="h-3.5 w-3.5 text-red-500 animate-pulse" />
              <span>Record Voice</span>
            </button>

            <span className="text-[11px] font-mono text-muted-foreground hidden sm:inline border-l border-border pl-2">
              Spoken Language:
            </span>
          </div>

          {/* Language Selector Pills */}
          <div className="flex items-center gap-1">
            <Languages className="h-3 w-3 text-muted-foreground mr-0.5 sm:hidden" />
            {LANGUAGE_OPTIONS.map((opt) => {
              const isSelected = selectedLang === opt.id;
              return (
                <button
                  key={opt.id}
                  type="button"
                  disabled={disabled}
                  onClick={() => setSelectedLang(opt.id)}
                  title={`Record voice in ${opt.label}`}
                  className={cn(
                    "px-2.5 py-1 rounded text-xs font-mono transition-all cursor-pointer",
                    isSelected
                      ? "bg-foreground text-background font-bold shadow-xs scale-102"
                      : "bg-muted hover:bg-muted/80 text-muted-foreground hover:text-foreground border border-border/60",
                  )}
                >
                  <span>{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

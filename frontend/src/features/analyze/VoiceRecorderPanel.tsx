import { motion, AnimatePresence } from "framer-motion";
import {
  Mic,
  Square,
  Loader2,
  AlertCircle,
  X,
  Volume2,
  CheckCircle2,
} from "lucide-react";
import { useVoiceRecorder, VoiceRecorderState, getLanguageLabel } from "@/hooks/useVoiceRecorder";
import { TranscribeResult } from "@/lib/speechApi";
import { cn } from "@/lib/utils";

interface VoiceRecorderPanelProps {
  onTranscriptReceived: (transcript: string, languageInfo: VoiceRecorderState["detectedLanguage"]) => void;
  disabled?: boolean;
}

export function VoiceRecorderPanel({
  onTranscriptReceived,
  disabled = false,
}: VoiceRecorderPanelProps) {
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
    onTranscriptionSuccess: (result: TranscribeResult) => {
      onTranscriptReceived(result.transcript, {
        code: result.language,
        label: getLanguageLabel(result.language),
        confidence: Math.round(result.language_probability * 100),
      });
    },
  });

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
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
                  Recording Audio ({formatTime(recordingSeconds)})
                </span>
                <span className="text-[11px] text-muted-foreground font-mono">
                  Speak your legal problem in English, हिन्दी, or ಕನ್ನಡ...
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
              <button
                type="button"
                onClick={stopRecording}
                className="inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-md bg-red-600 hover:bg-red-700 text-white font-mono text-xs font-bold uppercase shadow transition-all active:scale-95"
              >
                <Square className="h-3 w-3 fill-current" />
                <span>Done Recording</span>
              </button>

              <button
                type="button"
                onClick={cancelRecording}
                className="inline-flex items-center justify-center gap-1 px-2.5 py-1.5 rounded-md border border-border hover:bg-muted font-mono text-xs text-muted-foreground hover:text-foreground transition-all"
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
                Transcribing Speech via Whisper AI…
              </span>
              <span className="text-[11px] text-muted-foreground font-mono">
                Detecting English, Hindi, or Kannada and generating text locally.
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
              className="text-muted-foreground hover:text-foreground p-0.5"
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
              Review and edit below before submitting
            </span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Microphone Action Trigger (Shown when idle) */}
      {!isRecording && !isTranscribing && (
        <div className="flex items-center justify-between gap-2 pb-1">
          <button
            type="button"
            disabled={disabled}
            onClick={startRecording}
            className={cn(
              "inline-flex items-center gap-2 px-3 py-1.5 rounded-md border border-border/80 bg-muted/60 hover:bg-muted text-foreground font-mono text-xs font-semibold transition-all shadow-2xs hover:border-[#00c5ff]/60 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed",
            )}
          >
            <Mic className="h-3.5 w-3.5 text-red-500" />
            <span>Voice Input (Record)</span>
            <span className="hidden sm:inline-block text-[10px] text-muted-foreground border-l border-border pl-1.5">
              EN • हिन्दी • ಕನ್ನಡ
            </span>
          </button>

          <span className="text-[11px] font-mono text-muted-foreground hidden sm:inline">
            Speak in your language • Whisper local AI
          </span>
        </div>
      )}
    </div>
  );
}

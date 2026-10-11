import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Loader2, Scale } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { VoiceRecorderPanel } from "./VoiceRecorderPanel";
import { VoiceRecorderState } from "@/hooks/useVoiceRecorder";
import { cn } from "@/lib/utils";

const MIN = 20;
const MAX = 2000;

export function ScenarioInput({
  onSubmit,
  loading,
  initialValue = "",
}: {
  onSubmit: (scenario: string) => void;
  loading: boolean;
  initialValue?: string;
}) {
  const [value, setValue] = useState(initialValue);
  const [voiceLanguage, setVoiceLanguage] = useState<VoiceRecorderState["detectedLanguage"]>(null);

  const trimmed = value.trim();
  const len = trimmed.length;
  const tooShort = len > 0 && len < MIN;
  const tooLong = len > MAX;
  const canSubmit = len >= MIN && len <= MAX && !loading;

  const handleVoiceTranscript = (transcript: string, langInfo: VoiceRecorderState["detectedLanguage"]) => {
    setVoiceLanguage(langInfo);
    // If textarea is empty, set directly. If non-empty, append with a space.
    setValue((prev) => {
      const prevTrimmed = prev.trim();
      return prevTrimmed ? `${prevTrimmed}\n\n${transcript.trim()}` : transcript.trim();
    });
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (canSubmit) onSubmit(trimmed);
      }}
      className="w-full"
    >
      {/* Voice Complaint Recorder */}
      <VoiceRecorderPanel
        onTranscriptReceived={handleVoiceTranscript}
        disabled={loading}
      />

      <div className="relative rounded-xl border-2 border-border bg-card p-2 shadow-sm transition-colors focus-within:border-black dark:focus-within:border-[#00c5ff]">
        <span className="canvas-handle -top-1.5 -left-1.5" />
        <span className="canvas-handle -top-1.5 -right-1.5" />
        <span className="canvas-handle -bottom-1.5 -left-1.5" />
        <span className="canvas-handle -bottom-1.5 -right-1.5" />
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          maxLength={MAX + 200}
          placeholder="Describe your situation in plain words (English, हिन्दी, or ಕನ್ನಡ)... You can also record your voice above."
          aria-label="Describe your situation"
          aria-invalid={tooShort || tooLong}
          className="min-h-[200px] sm:min-h-[220px] bg-transparent border-0 text-base focus-visible:ring-0 focus-visible:outline-none resize-y pb-10"
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && canSubmit) {
              onSubmit(trimmed);
            }
          }}
        />

        {/* Bottom Bar inside the box */}
        <div className="absolute bottom-3 left-4 right-4 flex items-center justify-between text-xs font-mono text-muted-foreground select-none">
          <div className="flex items-center gap-3">
            <span
              className={cn(
                "tabular-nums transition-colors font-medium",
                tooShort && "text-amber-500",
                tooLong && "text-destructive",
              )}
            >
              {tooShort
                ? `${MIN - len} more characters needed`
                : tooLong
                  ? `${len - MAX} over limit`
                  : `${len} / ${MAX}`}
            </span>

            {len > 0 && (
              <button
                type="button"
                onClick={() => {
                  setValue("");
                  setVoiceLanguage(null);
                }}
                className="text-[11px] text-muted-foreground hover:text-foreground underline decoration-dotted transition-colors"
              >
                Clear
              </button>
            )}
          </div>

          <span className="hidden sm:inline opacity-70">
            Press Ctrl + Enter to submit
          </span>
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs font-mono text-muted-foreground flex items-center gap-2">
          {voiceLanguage ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 font-bold">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              Voice Input: {voiceLanguage.label} ({voiceLanguage.confidence}% confidence)
            </span>
          ) : (
            <>
              <span className="h-2 w-2 rounded-full bg-[#10b981]" />
              <span>Supports English, हिन्दी, &amp; ಕನ್ನಡ</span>
            </>
          )}
        </div>

        <motion.div whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
          <button
            type="submit"
            disabled={!canSubmit}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg bg-black text-white dark:bg-white dark:text-black font-mono text-xs font-bold tracking-wider uppercase shadow-md hover:bg-neutral-800 dark:hover:bg-neutral-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin text-[#00c5ff]" />
                <span>ANALYZING STATUTES…</span>
              </>
            ) : (
              <>
                <Scale className="h-4 w-4 text-[#00c5ff]" />
                <span>RUN LEGAL ANALYSIS</span>
                <ArrowRight className="h-4 w-4 ml-1" />
              </>
            )}
          </button>
        </motion.div>
      </div>
    </form>
  );
}

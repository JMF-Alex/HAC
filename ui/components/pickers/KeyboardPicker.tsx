import { keyLabel } from "../../api";
import { cx } from "../../lib/cx";

type KeyDef = [id: string | null, units: number, label?: string];

const chars = (row: string) => [...row].map((k): KeyDef => [k, 1]);

const ROWS: KeyDef[][] = [
  [["esc", 1, "Esc"], ...chars("1234567890"), ["backspace", 2, "⌫"]],
  [["tab", 1.5, "Tab"], ...chars("qwertyuiop"), [null, 1.5]],
  [[null, 1.75], ...chars("asdfghjkl"), ["enter", 2.25, "Enter"]],
  [["shift", 2.25, "Shift"], ...chars("zxcvbnm"), ["shift", 1.75, "Shift"], ["up", 1, "↑"]],
  [["ctrl", 1.25, "Ctrl"], ["alt", 1.25, "Alt"], ["space", 7.5, "Space"], ["left", 1, "←"], ["down", 1, "↓"], ["right", 1, "→"]],
];

const keyClass = "h-8 min-w-0 truncate rounded-md px-0.5 text-[11px] font-medium";

export function KeyboardPicker({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  return (
    <div className="mx-auto flex w-full max-w-md flex-col gap-0.75 rounded-lg bg-zinc-950/50 p-2.5 ring-1 ring-white/4 ring-inset">
      {ROWS.map((row, r) => (
        <div key={r} className="grid grid-cols-52 gap-0.75">
          {row.map(([id, units, label], i) => {
            const span = { gridColumn: `span ${units * 4}` };
            if (!id) return <span key={i} aria-hidden style={span} className={cx(keyClass, "bg-zinc-900/60 ring-1 ring-white/3 ring-inset")} />;
            return (
              <button
                key={i}
                type="button"
                title={keyLabel(id)}
                aria-label={keyLabel(id)}
                aria-pressed={value === id}
                onClick={() => onChange(id)}
                style={span}
                className={cx(
                  keyClass,
                  "cursor-pointer bg-zinc-800 text-zinc-300 transition",
                  "shadow-[inset_0_-2px_0_rgb(0_0_0/0.45)] ring-1 ring-white/5 ring-inset hover:bg-zinc-700 hover:text-white",
                  "aria-pressed:bg-violet-500 aria-pressed:text-white aria-pressed:ring-violet-300/40",
                  "focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-violet-400",
                  "disabled:cursor-not-allowed disabled:opacity-50",
                )}
              >
                {label ?? id.toUpperCase()}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}

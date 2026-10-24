import { Hand, MousePointerClick, type LucideIcon } from "lucide-react";
import type { Mode } from "../../api";
import { cx } from "../../lib/cx";

const MODES: { value: Mode; title: string; description: string; icon: LucideIcon }[] = [
  { value: "Click", title: "Click", description: "Press and release at every interval", icon: MousePointerClick },
  { value: "Hold", title: "Hold", description: "Keep it pressed until you stop", icon: Hand },
];

export function ModePicker({ value, onChange }: { value: Mode; onChange: (mode: Mode) => void }) {
  return (
    <div role="radiogroup" className="grid grid-cols-2 gap-2.5">
      {MODES.map(({ value: mode, title, description, icon: Icon }) => (
        <button
          key={mode}
          type="button"
          role="radio"
          aria-checked={mode === value}
          onClick={() => onChange(mode)}
          className={cx(
            "group relative flex cursor-pointer flex-col items-start gap-2.5 rounded-lg p-3 text-left ring-1 ring-white/10 transition ring-inset",
            "hover:bg-white/[0.03] aria-checked:bg-violet-500/10 aria-checked:ring-violet-500/60",
            "disabled:cursor-not-allowed disabled:opacity-50",
          )}
        >
          <span className="grid size-8 place-items-center rounded-md bg-zinc-800 text-zinc-400 transition group-aria-checked:bg-violet-500 group-aria-checked:text-white">
            <Icon className="size-4" />
          </span>
          <span>
            <span className="block text-sm font-semibold">{title}</span>
            <span className="mt-0.5 block text-xs leading-snug text-zinc-500">{description}</span>
          </span>
          <span className="absolute top-3 right-3 size-3.5 rounded-full ring-1 ring-white/20 transition group-aria-checked:bg-violet-500 group-aria-checked:ring-violet-500/25" />
        </button>
      ))}
    </div>
  );
}

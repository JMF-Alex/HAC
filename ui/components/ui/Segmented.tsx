import type { LucideIcon } from "lucide-react";
import { cx, focusRing } from "../../lib/cx";

export interface Option<T extends string> {
  value: T;
  label: string;
  icon?: LucideIcon;
}

export function Segmented<T extends string>({
  options,
  value,
  onChange,
  className,
}: {
  options: readonly Option<T>[];
  value: T;
  onChange: (value: T) => void;
  className?: string;
}) {
  return (
    <div role="radiogroup" className={cx("flex gap-0.5 rounded-lg bg-zinc-950/60 p-0.5 ring-1 ring-white/[0.06] ring-inset", className)}>
      {options.map(({ value: v, label, icon: Icon }) => (
        <button
          key={v}
          type="button"
          role="radio"
          aria-checked={v === value}
          onClick={() => onChange(v)}
          className={cx(
            "flex h-8 flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-md px-3 text-xs font-semibold text-zinc-400 transition",
            "hover:text-zinc-100 aria-checked:bg-zinc-700/70 aria-checked:text-white aria-checked:shadow-sm",
            "disabled:cursor-not-allowed disabled:opacity-50",
            focusRing,
          )}
        >
          {Icon && <Icon className="size-3.5" />}
          {label}
        </button>
      ))}
    </div>
  );
}

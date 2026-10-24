import { useEffect, useState } from "react";
import { cx } from "../../lib/cx";

export function NumberInput({
  value,
  onChange,
  suffix,
  className,
}: {
  value: number;
  onChange: (value: number) => void;
  suffix?: string;
  className?: string;
}) {
  const [draft, setDraft] = useState(String(value));
  const [focused, setFocused] = useState(false);
  useEffect(() => {
    if (!focused) setDraft(String(value));
  }, [value, focused]);

  return (
    <label
      className={cx(
        "flex h-9 items-center gap-2 rounded-lg bg-zinc-950/60 px-3 ring-1 ring-white/10 transition ring-inset",
        "focus-within:ring-2 focus-within:ring-violet-500 has-disabled:opacity-50",
        className,
      )}
    >
      <input
        inputMode="decimal"
        value={draft}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        onKeyDown={(e) => e.key === "Enter" && e.currentTarget.blur()}
        onChange={(e) => {
          setDraft(e.target.value);
          const raw = e.target.value.trim().replace(",", ".");
          const number = Number(raw);
          if (raw !== "" && Number.isFinite(number)) onChange(number);
        }}
        className="w-full min-w-0 bg-transparent text-sm text-zinc-100 tabular-nums outline-none select-text disabled:cursor-not-allowed"
      />
      {suffix && <span className="shrink-0 text-xs font-medium text-zinc-500">{suffix}</span>}
    </label>
  );
}

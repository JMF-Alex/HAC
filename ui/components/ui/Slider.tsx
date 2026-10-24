import { cx, focusRing } from "../../lib/cx";

export function Slider({
  value,
  min,
  max,
  step,
  onChange,
  label,
}: {
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (value: number) => void;
  label: string;
}) {
  const pct = ((value - min) / (max - min)) * 100;
  return (
    <input
      type="range"
      aria-label={label}
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      style={{ background: `linear-gradient(to right, var(--color-violet-500) ${pct}%, var(--color-zinc-800) ${pct}%)` }}
      className={cx(
        "h-1.5 w-full cursor-pointer appearance-none rounded-full disabled:opacity-50",
        "[&::-webkit-slider-thumb]:size-4 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full",
        "[&::-webkit-slider-thumb]:bg-white [&::-webkit-slider-thumb]:shadow-md [&::-webkit-slider-thumb]:ring-4",
        "[&::-webkit-slider-thumb]:ring-violet-500/30 [&::-webkit-slider-thumb]:transition hover:[&::-webkit-slider-thumb]:ring-violet-500/50",
        focusRing,
      )}
    />
  );
}

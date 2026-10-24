import { cx, focusRing } from "../../lib/cx";

export function Switch({ checked, onChange, label }: { checked: boolean; onChange: (v: boolean) => void; label: string }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      onClick={() => onChange(!checked)}
      className={cx(
        "group relative h-5 w-9 shrink-0 cursor-pointer rounded-full bg-zinc-700 transition-colors aria-checked:bg-violet-500",
        focusRing,
      )}
    >
      <span className="absolute top-0.5 left-0.5 size-4 rounded-full bg-white shadow transition-transform group-aria-checked:translate-x-4" />
    </button>
  );
}

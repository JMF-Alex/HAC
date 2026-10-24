import { cx } from "../../lib/cx";

const zoneClass = "cursor-pointer fill-zinc-800 stroke-zinc-600 transition hover:fill-zinc-700 aria-pressed:fill-violet-500 aria-pressed:stroke-violet-300 outline-none focus-visible:stroke-violet-300";

export function MousePicker({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  const zones = [
    { key: "mouse_left", label: "Left", d: "M58 12 C 30 14 14 34 14 68 V 80 H 58 Z" },
    { key: "mouse_right", label: "Right", d: "M62 12 C 90 14 106 34 106 68 V 80 H 62 Z" },
  ];
  const pick = (key: string) => (e: React.SyntheticEvent) => {
    if (!(e.currentTarget as Element).closest("fieldset:disabled")) onChange(key);
  };
  return (
    <div className="flex items-center gap-6">
      <svg viewBox="0 0 120 192" className="h-44 shrink-0 drop-shadow-xl" aria-label="Mouse buttons">
        <path d="M60 10 C 26 10 12 34 12 70 V 126 C 12 162 34 182 60 182 C 86 182 108 162 108 126 V 70 C 108 34 94 10 60 10 Z" className="fill-zinc-900 stroke-zinc-600" strokeWidth="2" />
        {zones.map((z) => (
          <path
            key={z.key}
            d={z.d}
            role="button"
            tabIndex={0}
            aria-label={`${z.label} button`}
            aria-pressed={value === z.key}
            onClick={pick(z.key)}
            onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && pick(z.key)(e)}
            className={zoneClass}
            strokeWidth="1.5"
          />
        ))}
        <rect
          x="52"
          y="26"
          width="16"
          height="32"
          rx="8"
          role="button"
          tabIndex={0}
          aria-label="Middle button (wheel)"
          aria-pressed={value === "mouse_middle"}
          onClick={pick("mouse_middle")}
          onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && pick("mouse_middle")(e)}
          className={zoneClass}
          strokeWidth="1.5"
        />
        <path d="M44 150 H 76" className="stroke-zinc-700" strokeWidth="2" strokeLinecap="round" />
      </svg>
      <div role="radiogroup" className="flex flex-1 flex-col gap-1.5">
        {[
          ["mouse_left", "Left button", "Primary click"],
          ["mouse_middle", "Middle button", "Wheel click"],
          ["mouse_right", "Right button", "Secondary click"],
        ].map(([key, title, hint]) => (
          <button
            key={key}
            type="button"
            role="radio"
            aria-checked={value === key}
            onClick={() => onChange(key)}
            className="flex cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left ring-1 ring-white/[0.06] transition ring-inset hover:bg-white/[0.03] disabled:opacity-50 aria-checked:bg-violet-500/10 aria-checked:ring-violet-500/50"
          >
            <span>
              <span className="block text-sm font-medium">{title}</span>
              <span className="block text-xs text-zinc-500">{hint}</span>
            </span>
            <span className={cx("size-2 rounded-full", value === key ? "bg-violet-400" : "bg-zinc-700")} />
          </button>
        ))}
      </div>
    </div>
  );
}

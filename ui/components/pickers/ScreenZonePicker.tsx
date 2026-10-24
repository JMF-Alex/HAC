import { ArrowDownLeft, ArrowDownRight, ArrowUpLeft, ArrowUpRight, type LucideIcon } from "lucide-react";
import type { Failsafe } from "../../api";
import { cx } from "../../lib/cx";

const ZONES: { value: Exclude<Failsafe, "Off">; place: string; corner: string; icon: LucideIcon }[] = [
  { value: "Top-left", place: "top-0 left-0", corner: "rounded-br-2xl", icon: ArrowUpLeft },
  { value: "Top-right", place: "top-0 right-0", corner: "rounded-bl-2xl", icon: ArrowUpRight },
  { value: "Bottom-left", place: "bottom-0 left-0", corner: "rounded-tr-2xl", icon: ArrowDownLeft },
  { value: "Bottom-right", place: "right-0 bottom-0", corner: "rounded-tl-2xl", icon: ArrowDownRight },
];

export function ScreenZonePicker({ value, onChange }: { value: Failsafe; onChange: (value: Failsafe) => void }) {
  return (
    <div className="flex w-full flex-col items-center">
      <div className="w-full max-w-md rounded-xl bg-zinc-800 p-2 shadow-2xl shadow-black/50 ring-1 ring-white/10">
        <div className="relative aspect-video overflow-hidden rounded-md bg-zinc-950 bg-[radial-gradient(circle_at_30%_25%,rgb(139_92_246/0.16),transparent_55%),radial-gradient(circle_at_80%_90%,rgb(56_189_248/0.08),transparent_50%)]">
          <div className="absolute inset-0 bg-[linear-gradient(rgb(255_255_255/0.035)_1px,transparent_1px),linear-gradient(90deg,rgb(255_255_255/0.035)_1px,transparent_1px)] bg-size-[24px_24px]" />
          <div className="absolute inset-0 grid place-items-center p-10 text-center">
            {value === "Off" ? (
              <p className="text-xs text-zinc-500">Pick a corner to enable the fail-safe</p>
            ) : (
              <p className="text-xs text-zinc-400">
                Move the pointer to the <span className="font-semibold text-rose-300">{value.toLowerCase()}</span> corner
                to stop instantly
              </p>
            )}
          </div>
          {ZONES.map(({ value: zone, place, corner, icon: Icon }) => {
            const selected = value === zone;
            return (
              <button
                key={zone}
                type="button"
                aria-pressed={selected}
                aria-label={`${zone} corner`}
                title={selected ? "Click to turn the fail-safe off" : `Stop at the ${zone.toLowerCase()} corner`}
                onClick={() => onChange(selected ? "Off" : zone)}
                className={cx(
                  "group absolute grid h-[30%] w-[22%] cursor-pointer place-items-center border border-dashed transition",
                  place,
                  corner,
                  selected
                    ? "border-solid border-rose-400/80 bg-rose-500/25 text-rose-200 shadow-[inset_0_0_24px_rgb(244_63_94/0.35)]"
                    : "border-white/10 text-zinc-600 hover:border-violet-400/60 hover:bg-violet-500/10 hover:text-violet-300",
                )}
              >
                <Icon className="size-4" />
                {selected && <span className={cx("absolute size-2 animate-ping rounded-full bg-rose-400", place.replace(/(\w+)-0/g, "$1-1.5"))} />}
              </button>
            );
          })}
        </div>
      </div>
      <div className="h-4 w-14 bg-linear-to-b from-zinc-800 to-zinc-900" />
      <div className="h-1.5 w-32 rounded-full bg-zinc-800" />
    </div>
  );
}

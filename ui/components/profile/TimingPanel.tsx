import { Clock, Gauge, Hash, Hourglass, Infinity as InfinityIcon, Shuffle, Timer, type LucideIcon } from "lucide-react";
import { useState } from "react";
import { api, type LimitKind } from "../../api";
import { cx } from "../../lib/cx";
import { NumberInput, Panel, Segmented, SettingRow, Slider } from "../ui";
import { Locked } from "./Locked";
import type { ProfileProps } from "./types";

const PRESETS = [0.001, 0.01, 0.1, 1];

const LIMITS: { value: LimitKind; label: string; icon: LucideIcon }[] = [
  { value: "Never", label: "Never", icon: InfinityIcon },
  { value: "Clicks", label: "Clicks", icon: Hash },
  { value: "Time", label: "Time", icon: Clock },
];

const update = api.updateProfile;

export function TimingPanel({ profile, status }: ProfileProps) {
  const [unit, setUnit] = useState<"ms" | "s">(profile.interval < 1 ? "ms" : "s");
  const scale = unit === "ms" ? 1000 : 1;
  const hold = profile.mode === "Hold";
  const perSecond = 1 / profile.interval;
  const rate =
    perSecond >= 1
      ? `≈ ${perSecond.toLocaleString("en-US", { maximumFractionDigits: 1 })} clicks per second`
      : `1 click every ${Number(profile.interval.toPrecision(6))} s`;

  const kind = profile.limit_kind;
  const limitHint =
    kind === "Clicks" && hold
      ? "Click limits only apply in Click mode"
      : kind === "Never"
        ? "Runs until you stop it"
        : kind === "Clicks"
          ? "Stops by itself after this many clicks"
          : "Stops by itself after this many seconds";

  return (
    <Panel title="Timing" description="How fast it goes and when it stops" icon={Timer}>
      <Locked locked={status.locked} className="divide-y divide-white/5">
        <SettingRow icon={Gauge} title="Interval" description={hold ? "Not used in Hold mode" : rate}>
          <div className={cx("flex items-center gap-3", hold && "opacity-50")}>
            <div className="flex gap-1">
              {PRESETS.map((p) => (
                <button
                  key={p}
                  type="button"
                  aria-pressed={profile.interval === p}
                  onClick={() => update({ interval: p })}
                  className="h-7 cursor-pointer rounded-md px-2 text-xs font-medium text-zinc-400 tabular-nums ring-1 ring-white/10 transition ring-inset hover:bg-white/5 hover:text-zinc-100 disabled:opacity-50 aria-pressed:bg-violet-500/15 aria-pressed:text-violet-200 aria-pressed:ring-violet-500/50"
                >
                  {p < 1 ? `${p * 1000} ms` : `${p} s`}
                </button>
              ))}
            </div>
            <NumberInput
              value={Number((profile.interval * scale).toPrecision(10))}
              onChange={(n) => update({ interval: n / scale })}
              className="w-28"
            />
            <Segmented
              options={[
                { value: "ms", label: "ms" },
                { value: "s", label: "s" },
              ]}
              value={unit}
              onChange={setUnit}
              className="w-20"
            />
          </div>
        </SettingRow>

        <SettingRow icon={Shuffle} title="Random variation" description="Up to ± this much per delay">
          <div className="w-64">
            <Slider label="Random variation" value={profile.jitter} min={0} max={100} step={1} onChange={(jitter) => update({ jitter })} />
          </div>
          <NumberInput value={profile.jitter} suffix="%" onChange={(jitter) => update({ jitter })} className="w-24" />
        </SettingRow>

        <SettingRow icon={Hourglass} title="Start delay" description="Countdown before the first click">
          <div className="w-64">
            <Slider label="Start delay" value={profile.start_delay} min={0} max={60} step={0.5} onChange={(start_delay) => update({ start_delay })} />
          </div>
          <NumberInput value={profile.start_delay} suffix="s" onChange={(start_delay) => update({ start_delay })} className="w-24" />
        </SettingRow>

        <SettingRow
          icon={Clock}
          title="Stop after"
          description={<span className={cx(kind === "Clicks" && hold && "text-amber-400")}>{limitHint}</span>}
        >
          {kind !== "Never" && (
            <NumberInput
              value={profile.limit_value}
              suffix={kind === "Clicks" ? "clicks" : "s"}
              onChange={(limit_value) => update({ limit_value })}
              className="w-32 animate-fade"
            />
          )}
          <Segmented options={LIMITS} value={kind} onChange={(limit_kind) => update({ limit_kind })} className="w-72" />
        </SettingRow>
      </Locked>
    </Panel>
  );
}

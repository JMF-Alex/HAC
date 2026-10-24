import { Activity, Gauge, Hash, Timer } from "lucide-react";
import { formatDuration, type Profile, type Status } from "../../api";
import { Stat } from "./Stat";

export function Telemetry({ profile, status }: { profile: Profile; status: Status }) {
  const holding = profile.mode === "Hold";
  const rate = status.clicks > 1 && status.elapsed >= 1 ? status.clicks / status.elapsed : null;
  const kind = holding && profile.limit_kind === "Clicks" ? "Never" : profile.limit_kind;
  const progress =
    kind === "Clicks" ? status.clicks / profile.limit_value : kind === "Time" ? status.elapsed / profile.limit_value : 0;

  return (
    <div className="grid grid-cols-4 gap-3">
      <Stat label="Clicks" icon={Hash} value={holding ? "—" : status.clicks.toLocaleString("en-US")} footer={holding ? "Hold mode presses once" : "this run"} />
      <Stat
        label="Rate"
        icon={Gauge}
        value={rate === null ? "—" : rate.toFixed(1)}
        unit="/s"
        footer={holding ? "—" : `target ${(1 / profile.interval).toLocaleString("en-US", { maximumFractionDigits: 1 })}/s`}
      />
      <Stat
        label={status.kind === "waiting" ? "Starting in" : "Elapsed"}
        icon={Timer}
        value={status.kind === "waiting" ? status.countdown.toFixed(1) : formatDuration(status.elapsed)}
        unit={status.kind === "waiting" ? "s" : undefined}
        footer={profile.start_delay > 0 ? `${profile.start_delay} s start delay` : "no start delay"}
      />
      <Stat
        label="Stop after"
        icon={Activity}
        value={kind === "Never" ? "∞" : profile.limit_value.toLocaleString("en-US")}
        unit={kind === "Clicks" ? "clicks" : kind === "Time" ? "s" : undefined}
        footer={
          kind === "Never" ? (
            "runs until you stop it"
          ) : (
            <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-zinc-800">
              <div className="h-full rounded-full bg-violet-500 transition-[width] duration-200" style={{ width: `${Math.min(1, progress) * 100}%` }} />
            </div>
          )
        }
      />
    </div>
  );
}

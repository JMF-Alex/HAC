import { Play, ShieldCheck, Square } from "lucide-react";
import { api, formatInterval, keyLabel, type Failsafe, type Profile, type Status } from "../../api";
import { cx } from "../../lib/cx";
import { Button, Kbd, StatusBadge } from "../ui";

export function TopBar({
  name,
  profile,
  status,
  failsafe,
  onOpenSettings,
}: {
  name: string;
  profile: Profile;
  status: Status;
  failsafe: Failsafe;
  onOpenSettings: () => void;
}) {
  const active = status.kind === "running" || status.kind === "waiting";
  const label = status.kind === "waiting" ? "Cancel start" : active ? "Stop" : "Start";
  const summary = `${profile.mode} · ${keyLabel(profile.target_key)}${profile.mode === "Click" ? ` · every ${formatInterval(profile.interval)}` : ""}`;
  return (
    <header className="flex h-16 shrink-0 items-center gap-4 border-b border-white/5 px-6">
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2.5">
          <h1 className="truncate text-base font-semibold">{name}</h1>
          <StatusBadge kind={status.kind} />
          {failsafe !== "Off" && (
            <button
              type="button"
              title="Fail-safe corner (open settings)"
              onClick={onOpenSettings}
              className="inline-flex h-6 cursor-pointer items-center gap-1 rounded-full bg-rose-500/10 px-2.5 text-xs font-medium text-rose-300 ring-1 ring-rose-500/25 transition ring-inset hover:bg-rose-500/15"
            >
              <ShieldCheck className="size-3.5" />
              Fail-safe · {failsafe.toLowerCase()}
            </button>
          )}
        </div>
        <p className={cx("mt-0.5 truncate text-xs", status.kind === "error" ? "text-amber-400" : "text-zinc-500")}>
          {status.kind === "error" || status.kind === "done" ? status.message : summary}
        </p>
      </div>
      <Button size="lg" variant={active ? "danger" : "primary"} icon={active ? Square : Play} className="min-w-40" onClick={api.toggle}>
        {label}
        {profile.hotkey && <Kbd className="ml-1 bg-black/25 text-white/90 ring-white/20">{profile.hotkey}</Kbd>}
      </Button>
    </header>
  );
}

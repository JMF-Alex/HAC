import type { Status } from "../../api";
import { cx } from "../../lib/cx";

const badges: Record<Status["kind"], [string, string, string]> = {
  stopped: ["Idle", "bg-zinc-800 text-zinc-300 ring-white/10", "bg-zinc-500"],
  done: ["Idle", "bg-zinc-800 text-zinc-300 ring-white/10", "bg-zinc-500"],
  running: ["Running", "bg-emerald-500/10 text-emerald-300 ring-emerald-500/30", "bg-emerald-400 animate-pulse"],
  waiting: ["Starting", "bg-amber-500/10 text-amber-300 ring-amber-500/30", "bg-amber-400 animate-pulse"],
  error: ["Error", "bg-rose-500/10 text-rose-300 ring-rose-500/30", "bg-rose-400"],
};

export function StatusBadge({ kind }: { kind: Status["kind"] }) {
  const [label, style, dot] = badges[kind];
  return (
    <span className={cx("inline-flex h-6 items-center gap-1.5 rounded-full px-2.5 text-xs font-semibold ring-1 ring-inset", style)}>
      <span className={cx("size-1.5 rounded-full", dot)} />
      {label}
    </span>
  );
}

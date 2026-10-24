import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

export function Stat({ label, icon: Icon, value, unit, footer }: { label: string; icon: LucideIcon; value: ReactNode; unit?: string; footer?: ReactNode }) {
  return (
    <div className="flex flex-col rounded-xl bg-zinc-900/70 px-4 py-2.5 ring-1 ring-white/[0.06] ring-inset">
      <div className="flex items-center gap-1.5 text-xs font-medium text-zinc-400">
        <Icon className="size-3.5" />
        {label}
      </div>
      <div className="mt-1.5 flex items-baseline gap-1 text-2xl font-semibold text-zinc-50 tabular-nums">
        {value}
        {unit && <span className="text-xs font-medium text-zinc-500">{unit}</span>}
      </div>
      <div className="mt-1 h-4 text-xs text-zinc-500">{footer}</div>
    </div>
  );
}

import { Lock } from "lucide-react";
import type { ReactNode } from "react";
import { cx } from "../../lib/cx";

export function Locked({ locked, children, className }: { locked: boolean; children: ReactNode; className?: string }) {
  return (
    <fieldset disabled={locked} className={cx("relative min-w-0", className)}>
      {children}
    </fieldset>
  );
}

export function LockNotice({ locked }: { locked: boolean }) {
  if (!locked) return null;
  return (
    <div className="flex animate-fade items-center gap-2 rounded-lg bg-amber-500/10 px-3 py-2 text-xs text-amber-200 ring-1 ring-amber-500/20 ring-inset">
      <Lock className="size-3.5" />
      Settings are locked while clicking. Stop to edit them.
    </div>
  );
}

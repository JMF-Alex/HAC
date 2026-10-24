import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { cx } from "../../lib/cx";

export function Panel({
  title,
  description,
  icon: Icon,
  actions,
  className,
  children,
}: {
  title: string;
  description?: ReactNode;
  icon?: LucideIcon;
  actions?: ReactNode;
  className?: string;
  children: ReactNode;
}) {
  return (
    <section className={cx("flex flex-col rounded-xl bg-zinc-900/70 p-4 ring-1 ring-white/[0.06] ring-inset", className)}>
      <header className="mb-4 flex items-start gap-3">
        {Icon && (
          <span className="grid size-8 shrink-0 place-items-center rounded-lg bg-white/5 text-zinc-300 ring-1 ring-white/10 ring-inset">
            <Icon className="size-4" />
          </span>
        )}
        <div className="min-w-0 flex-1">
          <h3 className="text-sm font-semibold text-zinc-100">{title}</h3>
          {description && <p className="mt-0.5 text-xs text-zinc-500">{description}</p>}
        </div>
        {actions}
      </header>
      <div className="flex flex-1 flex-col">{children}</div>
    </section>
  );
}

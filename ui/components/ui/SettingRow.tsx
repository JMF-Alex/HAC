import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { cx } from "../../lib/cx";

export function SettingRow({
  icon: Icon,
  title,
  description,
  children,
  className,
}: {
  icon?: LucideIcon;
  title: string;
  description?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={cx("flex items-center gap-6 py-3 first:pt-0 last:pb-0", className)}>
      <div className="flex w-56 shrink-0 items-start gap-3">
        {Icon && <Icon className="mt-0.5 size-4 shrink-0 text-zinc-500" />}
        <div className="min-w-0">
          <div className="text-sm font-medium">{title}</div>
          {description && <div className="mt-0.5 text-xs text-zinc-500">{description}</div>}
        </div>
      </div>
      <div className="flex min-w-0 flex-1 items-center justify-end gap-3">{children}</div>
    </div>
  );
}

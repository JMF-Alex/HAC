import type { LucideIcon } from "lucide-react";
import { useEffect, type ReactNode } from "react";
import { cx } from "../../lib/cx";

export function Modal({
  title,
  description,
  icon: Icon,
  danger,
  className,
  onClose,
  children,
}: {
  title: string;
  description?: string;
  icon?: LucideIcon;
  danger?: boolean;
  className?: string;
  onClose: () => void;
  children: ReactNode;
}) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);
  return (
    <div
      className="fixed inset-0 z-50 grid animate-fade place-items-center bg-black/60 backdrop-blur-sm"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <div role="dialog" aria-modal aria-label={title} className={cx("w-104 animate-pop rounded-2xl bg-zinc-900 p-5 shadow-2xl ring-1 ring-white/10", className)}>
        <div className="mb-4 flex gap-3">
          {Icon && (
            <span
              className={cx(
                "grid size-9 shrink-0 place-items-center rounded-full",
                danger ? "bg-rose-500/15 text-rose-400" : "bg-white/5 text-zinc-300",
              )}
            >
              <Icon className="size-4" />
            </span>
          )}
          <div>
            <h2 className="text-base font-semibold">{title}</h2>
            {description && <p className="mt-1 text-sm text-zinc-400">{description}</p>}
          </div>
        </div>
        {children}
      </div>
    </div>
  );
}

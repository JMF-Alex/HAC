import type { LucideIcon } from "lucide-react";
import type { ButtonHTMLAttributes } from "react";
import { cx, focusRing } from "../../lib/cx";

export function IconButton({
  icon: Icon,
  label,
  danger,
  className,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { icon: LucideIcon; label: string; danger?: boolean }) {
  return (
    <button
      type="button"
      title={label}
      aria-label={label}
      {...props}
      className={cx(
        "grid size-7 cursor-pointer place-items-center rounded-md text-zinc-500 transition",
        danger ? "hover:bg-rose-500/15 hover:text-rose-400" : "hover:bg-white/10 hover:text-zinc-100",
        focusRing,
        className,
      )}
    >
      <Icon className="size-3.5" strokeWidth={2.25} />
    </button>
  );
}

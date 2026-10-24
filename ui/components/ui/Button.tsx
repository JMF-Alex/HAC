import type { LucideIcon } from "lucide-react";
import type { ButtonHTMLAttributes } from "react";
import { cx, focusRing } from "../../lib/cx";

const buttonVariants = {
  primary: "bg-violet-500 text-white shadow-lg shadow-violet-500/20 hover:bg-violet-400",
  danger: "bg-rose-500 text-white shadow-lg shadow-rose-500/20 hover:bg-rose-400",
  secondary: "bg-white/5 text-zinc-100 ring-1 ring-white/10 ring-inset hover:bg-white/10",
  ghost: "text-zinc-400 hover:bg-white/5 hover:text-zinc-100",
};

const buttonSizes = { sm: "h-7 gap-1.5 text-xs", md: "h-9 gap-2 text-sm", lg: "h-11 gap-2.5 text-sm" };
const buttonPadding = { sm: "px-2.5", md: "px-3.5", lg: "px-5" };
// a button with only an icon is a square of the same height
const iconOnlyWidth = { sm: "w-7", md: "w-9", lg: "w-11" };

export function Button({
  variant = "secondary",
  size = "md",
  icon: Icon,
  className,
  children,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof buttonSizes;
  icon?: LucideIcon;
}) {
  return (
    <button
      type="button"
      {...props}
      className={cx(
        "inline-flex shrink-0 cursor-pointer items-center justify-center rounded-lg font-semibold whitespace-nowrap transition",
        "active:scale-[0.98] disabled:pointer-events-none disabled:opacity-40",
        focusRing,
        buttonVariants[variant],
        buttonSizes[size],
        children == null ? iconOnlyWidth[size] : buttonPadding[size],
        className,
      )}
    >
      {Icon && <Icon className="size-4" strokeWidth={2.25} />}
      {children}
    </button>
  );
}

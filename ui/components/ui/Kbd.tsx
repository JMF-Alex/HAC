import type { ReactNode } from "react";
import { cx } from "../../lib/cx";

export function Kbd({ children, size = "sm", className }: { children: ReactNode; size?: "sm" | "lg"; className?: string }) {
  return (
    <kbd
      className={cx(
        "inline-flex items-center justify-center rounded-md bg-zinc-800 font-semibold text-zinc-200",
        "shadow-[inset_0_-2px_0_rgb(0_0_0/0.45)] ring-1 ring-white/10 ring-inset",
        size === "sm" ? "h-5 min-w-5 px-1.5 text-xs" : "h-12 min-w-16 px-4 text-lg",
        className,
      )}
    >
      {children}
    </kbd>
  );
}

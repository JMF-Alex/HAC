export const cx = (...classes: (string | false | null | undefined)[]) => classes.filter(Boolean).join(" ");

export const focusRing = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400";

import { cx } from "../../lib/cx";

function Key({
  id,
  label,
  value,
  onChange,
  className,
}: {
  id: string;
  label?: string;
  value: string;
  onChange: (key: string) => void;
  className?: string;
}) {
  return (
    <button
      type="button"
      aria-pressed={value === id}
      onClick={() => onChange(id)}
      className={cx(
        "h-8 min-w-8 cursor-pointer rounded-md bg-zinc-800 px-1.5 text-xs font-medium text-zinc-300 transition",
        "shadow-[inset_0_-2px_0_rgb(0_0_0/0.45)] ring-1 ring-white/5 ring-inset hover:bg-zinc-700 hover:text-white",
        "aria-pressed:bg-violet-500 aria-pressed:text-white aria-pressed:ring-violet-300/40",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
    >
      {label ?? id.toUpperCase()}
    </button>
  );
}

const ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

export function KeyboardPicker({ value, onChange }: { value: string; onChange: (key: string) => void }) {
  const key = (id: string, label?: string, className = "w-8") => (
    <Key key={id} id={id} label={label} value={value} onChange={onChange} className={className} />
  );
  return (
    <div className="mx-auto flex w-fit flex-col gap-1.5 rounded-lg bg-zinc-950/50 p-3 ring-1 ring-white/[0.04] ring-inset">
      {ROWS.map((row, i) => (
        <div key={row} className="flex gap-1.5" style={{ paddingLeft: `${i * 16}px` }}>
          {[...row].map((k) => key(k))}
        </div>
      ))}
      <div className="flex gap-1.5">
        {key("shift", "Shift", "w-14")}
        {key("ctrl", "Ctrl", "w-12")}
        {key("alt", "Alt", "w-12")}
        {key("space", "Space", "flex-1")}
      </div>
      <div className="flex gap-1.5">
        {key("tab", "Tab", "w-12")}
        {key("enter", "Enter", "w-14")}
        <span className="flex-1" />
        {key("left", "←")}
        {key("up", "↑")}
        {key("down", "↓")}
        {key("right", "→")}
      </div>
    </div>
  );
}

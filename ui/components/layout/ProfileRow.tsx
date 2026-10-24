import { Copy, Hand, MousePointerClick, Pencil, Trash2 } from "lucide-react";
import { useEffect, useRef } from "react";
import { api, formatInterval, keyLabel, type Profile } from "../../api";
import { cx } from "../../lib/cx";
import { IconButton, Kbd } from "../ui";

export interface RowActions {
  onRename: (name: string) => void;
  onDelete: (name: string) => void;
}

export function ProfileRow({
  name,
  profile,
  active,
  running,
  onRename,
  onDelete,
}: { name: string; profile: Profile; active: boolean; running: boolean } & RowActions) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (active) ref.current?.scrollIntoView({ block: "nearest" });
  }, [active]);
  const ModeIcon = profile.mode === "Hold" ? Hand : MousePointerClick;

  return (
    <div
      ref={ref}
      className={cx(
        "group relative rounded-lg transition-colors",
        active ? "bg-white/[0.06] ring-1 ring-white/10 ring-inset" : "hover:bg-white/[0.03]",
      )}
    >
      <button
        type="button"
        onClick={() => api.selectProfile(name)}
        className="flex w-full cursor-pointer items-center gap-3 rounded-lg px-2.5 py-2 text-left focus-visible:outline-2 focus-visible:outline-violet-400"
      >
        <span
          className={cx(
            "relative grid size-8 shrink-0 place-items-center rounded-md transition",
            active ? "bg-violet-500 text-white shadow-md shadow-violet-500/30" : "bg-zinc-800 text-zinc-400",
          )}
        >
          <ModeIcon className="size-4" />
          {running && (
            <span className="absolute -top-0.5 -right-0.5 size-2.5 rounded-full bg-emerald-400 ring-2 ring-zinc-900" />
          )}
        </span>
        <span className="min-w-0 flex-1">
          <span className={cx("block truncate text-sm font-medium", active ? "text-white" : "text-zinc-300")}>{name}</span>
          <span className="block truncate text-xs text-zinc-500">
            {keyLabel(profile.target_key)} · {formatInterval(profile.interval)}
          </span>
        </span>
        <Kbd className="transition group-focus-within:opacity-0 group-hover:opacity-0">{profile.hotkey || "—"}</Kbd>
      </button>
      <div className="absolute inset-y-0 right-1.5 flex items-center gap-0.5 opacity-0 pointer-events-none transition group-focus-within:pointer-events-auto group-focus-within:opacity-100 group-hover:pointer-events-auto group-hover:opacity-100">
        <IconButton icon={Pencil} label="Rename" onClick={() => onRename(name)} />
        <IconButton icon={Copy} label="Duplicate" onClick={() => api.duplicateProfile(name)} />
        <IconButton icon={Trash2} label="Delete" danger onClick={() => onDelete(name)} />
      </div>
    </div>
  );
}

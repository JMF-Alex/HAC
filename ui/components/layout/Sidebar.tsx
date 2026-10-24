import { Plus, Settings } from "lucide-react";
import type { Config } from "../../api";
import logo from "../../assets/logo.png";
import { Button, IconButton } from "../ui";
import { ProfileRow, type RowActions } from "./ProfileRow";

export function Sidebar({
  config,
  version,
  running,
  onAdd,
  onSettings,
  ...actions
}: { config: Config; version: string; running: boolean; onAdd: () => void; onSettings: () => void } & RowActions) {
  const names = Object.keys(config.profiles);
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-white/5 bg-zinc-900/40">
      <div className="flex h-16 shrink-0 items-center gap-3 border-b border-white/5 px-4">
        <img src={logo} alt="" className="size-8 rounded-lg ring-1 ring-white/10 [image-rendering:pixelated]" />
        <div className="min-w-0 flex-1">
          <div className="text-sm font-semibold">HAutoClicker</div>
          <div className="text-xs text-zinc-500">Version {version}</div>
        </div>
      </div>

      <div className="flex items-center justify-between px-4 pt-4 pb-2">
        <span className="flex items-center gap-2 text-xs font-medium text-zinc-400">
          Profiles
          <span className="rounded bg-white/5 px-1.5 py-px text-xs text-zinc-400">{names.length}</span>
        </span>
        <IconButton icon={Plus} label="New profile" onClick={onAdd} />
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-2 pb-2">
        {names.map((name) => (
          <ProfileRow
            key={name}
            name={name}
            profile={config.profiles[name]}
            active={name === config.active_profile}
            running={running && name === config.active_profile}
            {...actions}
          />
        ))}
      </nav>

      <div className="flex gap-2 border-t border-white/5 p-3">
        <Button icon={Plus} className="flex-1" onClick={onAdd}>
          New profile
        </Button>
        <Button icon={Settings} aria-label="Settings" title="Settings" onClick={onSettings} />
      </div>
    </aside>
  );
}

import { Circle, MousePointerClick } from "lucide-react";
import { api } from "../../api";
import { cx } from "../../lib/cx";
import { ModePicker } from "../pickers";
import { Button, Kbd, Panel } from "../ui";
import { Locked } from "./Locked";
import type { ProfileProps } from "./types";

export function ActionPanel({ profile, status }: ProfileProps) {
  const capturing = status.capturing;
  return (
    <Panel title="Action" description="What happens, and the key that starts it" icon={MousePointerClick} className="h-full">
      <Locked locked={status.locked}>
        <ModePicker value={profile.mode} onChange={(mode) => api.updateProfile({ mode })} />
      </Locked>
      <div className="mt-auto flex items-center gap-3 border-t border-white/5 pt-4">
        <Kbd size="lg" className={cx(capturing && "animate-pulse text-amber-300 ring-2 ring-amber-400/60")}>
          {capturing ? "…" : profile.hotkey || "—"}
        </Kbd>
        <div className="min-w-0 flex-1">
          <div className="text-sm font-medium">Hotkey</div>
          <p className={cx("mt-0.5 text-xs", capturing ? "text-amber-300" : "text-zinc-500")}>
            {capturing ? "Press any key now. Esc keeps the current one." : "Works from any window"}
          </p>
        </div>
        <Button size="sm" icon={Circle} className="[&_svg]:fill-rose-500 [&_svg]:text-rose-500" disabled={capturing} onClick={api.captureHotkey}>
          {capturing ? "Listening…" : "Record"}
        </Button>
      </div>
    </Panel>
  );
}

import { Pin, Settings2, ShieldCheck, Volume2 } from "lucide-react";
import { api, type Settings } from "../../api";
import { ScreenZonePicker } from "../pickers";
import { Button, SettingRow, Switch } from "../ui";
import { Modal } from "./Modal";

export function SettingsDialog({ settings, onClose }: { settings: Settings; onClose: () => void }) {
  const set = (patch: Partial<Settings>) => api.updateSettings({ ...settings, ...patch });
  return (
    <Modal title="Settings" description="These apply to every profile." icon={Settings2} onClose={onClose} className="w-xl">
      <section>
        <div className="mb-3 flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <ShieldCheck className="mt-0.5 size-4 shrink-0 text-zinc-500" />
            <div>
              <h3 className="text-sm font-medium">Fail-safe corner</h3>
              <p className="mt-0.5 text-xs text-zinc-500">Move the pointer into this corner to stop clicking at once</p>
            </div>
          </div>
          {settings.failsafe !== "Off" && (
            <Button size="sm" variant="ghost" onClick={() => set({ failsafe: "Off" })}>
              Turn off
            </Button>
          )}
        </div>
        <ScreenZonePicker value={settings.failsafe} onChange={(failsafe) => set({ failsafe })} />
      </section>

      <div className="mt-5 divide-y divide-white/5 border-t border-white/5 pt-4">
        <SettingRow icon={Pin} title="Always on top" description="Keep this window above the others">
          <Switch label="Always on top" checked={settings.always_on_top} onChange={(always_on_top) => set({ always_on_top })} />
        </SettingRow>
        <SettingRow icon={Volume2} title="Sound" description="Beep when clicking starts or stops">
          <Switch label="Sound" checked={settings.sound} onChange={(sound) => set({ sound })} />
        </SettingRow>
      </div>

      <div className="mt-5 flex justify-end">
        <Button variant="primary" onClick={onClose}>
          Done
        </Button>
      </div>
    </Modal>
  );
}

import { getVersion } from "@tauri-apps/api/app";
import { useEffect, useState } from "react";
import { api, uniqueName, useAppState } from "./api";
import { ConfirmDialog, NameDialog, SettingsDialog } from "./components/dialogs";
import { Sidebar, Telemetry, TopBar } from "./components/layout";
import { ProfileView } from "./components/profile";

type Dialog =
  | { kind: "add" }
  | { kind: "rename"; name: string }
  | { kind: "delete"; name: string }
  | { kind: "settings" }
  | { kind: "message"; title: string; text: string };

export default function App() {
  const { config, status } = useAppState();
  const [dialog, setDialog] = useState<Dialog | null>(null);
  const [version, setVersion] = useState("");

  useEffect(() => {
    getVersion().then(setVersion);
  }, []);

  // hotkeys are ignored while a dialog is open
  useEffect(() => {
    api.setDialogOpen(dialog !== null);
  }, [dialog]);

  if (!config || !status) return null;

  const active = config.active_profile;
  const profile = config.profiles[active];
  const names = Object.keys(config.profiles);
  const running = status.kind === "running" || status.kind === "waiting";
  const close = () => setDialog(null);
  const openSettings = () => setDialog({ kind: "settings" });

  return (
    <>
      <div className="flex h-full" inert={dialog !== null}>
        <Sidebar
          config={config}
          version={version}
          running={running}
          onAdd={() => setDialog({ kind: "add" })}
          onSettings={openSettings}
          onRename={(name) => setDialog({ kind: "rename", name })}
          onDelete={(name) =>
            setDialog(
              names.length === 1
                ? { kind: "message", title: "Can't delete this profile", text: "You need at least one profile." }
                : { kind: "delete", name },
            )
          }
        />

        <main className="flex min-w-0 flex-1 flex-col bg-[radial-gradient(ellipse_at_top,rgb(139_92_246/0.07),transparent_60%)]">
          <TopBar name={active} profile={profile} status={status} failsafe={config.settings.failsafe} onOpenSettings={openSettings} />
          <div className="flex-1 space-y-4 overflow-x-hidden overflow-y-auto px-6 py-5">
            <Telemetry profile={profile} status={status} />
            {/* remount per profile so local view state (mouse/keyboard, ms/s) follows the profile */}
            <div key={active} className="animate-fade">
              <ProfileView profile={profile} status={status} />
            </div>
          </div>
        </main>
      </div>

      {dialog?.kind === "add" && (
        <NameDialog title="New profile" initial={uniqueName("Profile", names)} confirm="Create profile" onSubmit={api.addProfile} onClose={close} />
      )}
      {dialog?.kind === "rename" && (
        <NameDialog
          title="Rename profile"
          initial={dialog.name}
          confirm="Save"
          onSubmit={(newName) => api.renameProfile(dialog.name, newName)}
          onClose={close}
        />
      )}
      {dialog?.kind === "delete" && (
        <ConfirmDialog
          title="Delete profile?"
          message={`“${dialog.name}” and its settings will be removed. This can't be undone.`}
          confirm="Delete profile"
          danger
          onConfirm={() =>
            api.deleteProfile(dialog.name).catch((err) => setDialog({ kind: "message", title: "Can't delete this profile", text: String(err) }))
          }
          onClose={close}
        />
      )}
      {dialog?.kind === "settings" && <SettingsDialog settings={config.settings} onClose={close} />}
      {dialog?.kind === "message" && <ConfirmDialog title={dialog.title} message={dialog.text} onClose={close} />}
    </>
  );
}

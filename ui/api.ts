import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { useEffect, useState } from "react";

export type Mode = "Click" | "Hold";
export type LimitKind = "Never" | "Clicks" | "Time";
export type Failsafe = "Off" | "Top-left" | "Top-right" | "Bottom-left" | "Bottom-right";

export interface Profile {
  interval: number;
  hotkey: string;
  mode: Mode;
  target_key: string;
  jitter: number;
  limit_kind: LimitKind;
  limit_value: number;
  start_delay: number;
}

export interface Settings {
  failsafe: Failsafe;
  always_on_top: boolean;
  sound: boolean;
}

export interface Config {
  version: number;
  active_profile: string;
  profiles: Record<string, Profile>;
  settings: Settings;
}

export interface Status {
  kind: "stopped" | "running" | "waiting" | "error" | "done";
  message: string | null;
  locked: boolean;
  capturing: boolean;
  clicks: number;
  /** seconds of clicking in the current (or last) run */
  elapsed: number;
  /** seconds left on the start delay */
  countdown: number;
}

export const api = {
  toggle: () => invoke("toggle"),
  selectProfile: (name: string) => invoke("select_profile", { name }),
  addProfile: (name: string) => invoke("add_profile", { name }),
  duplicateProfile: (name: string) => invoke("duplicate_profile", { name }),
  renameProfile: (name: string, newName: string) => invoke("rename_profile", { name, newName }),
  deleteProfile: (name: string) => invoke("delete_profile", { name }),
  updateProfile: (patch: Partial<Profile>) => invoke("update_profile", { patch }),
  updateSettings: (settings: Settings) => invoke("update_settings", { settings }),
  captureHotkey: () => invoke("capture_hotkey"),
  setDialogOpen: (open: boolean) => invoke("set_dialog_open", { open }),
};

export function useAppState() {
  const [config, setConfig] = useState<Config | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  useEffect(() => {
    const unlisten = [
      listen<Config>("config", (e) => setConfig(e.payload)),
      listen<Status>("status", (e) => setStatus(e.payload)),
    ];
    invoke<{ config: Config; status: Status }>("get_state").then((s) => {
      setConfig(s.config);
      setStatus(s.status);
    });
    return () => unlisten.forEach((p) => p.then((off) => off()));
  }, []);
  return { config, status };
}

const capitalize = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export function keyLabel(key: string) {
  if (key.startsWith("mouse_")) return `${capitalize(key.slice(6))} mouse`;
  return key.length === 1 ? key.toUpperCase() : capitalize(key);
}

const g = (n: number) => String(Number(n.toPrecision(6)));

export const formatInterval = (seconds: number) => (seconds < 1 ? `${g(seconds * 1000)} ms` : `${g(seconds)} s`);

export function uniqueName(base: string, existing: string[]) {
  const taken = new Set(existing.map((n) => n.toLowerCase()));
  if (!taken.has(base.toLowerCase())) return base;
  let i = 2;
  while (taken.has(`${base} ${i}`.toLowerCase())) i++;
  return `${base} ${i}`;
}

export function formatDuration(seconds: number) {
  const total = Math.floor(seconds);
  const [h, m, s] = [Math.floor(total / 3600), Math.floor(total / 60) % 60, total % 60];
  const pad = (n: number) => String(n).padStart(2, "0");
  return h ? `${h}:${pad(m)}:${pad(s)}` : `${pad(m)}:${pad(s)}`;
}

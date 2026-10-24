import { Crosshair, Keyboard, Mouse } from "lucide-react";
import { useState } from "react";
import { api, keyLabel } from "../../api";
import { KeyboardPicker, MousePicker } from "../pickers";
import { Panel, Segmented } from "../ui";
import { Locked } from "./Locked";
import type { ProfileProps } from "./types";

export function TargetPanel({ profile, status }: ProfileProps) {
  const [device, setDevice] = useState<"mouse" | "keyboard">(profile.target_key.startsWith("mouse_") ? "mouse" : "keyboard");
  const pick = (target_key: string) => api.updateProfile({ target_key });

  return (
    <Locked locked={status.locked}>
      <Panel
        title="Target"
        description={`Pressing ${keyLabel(profile.target_key)}`}
        icon={Crosshair}
        className="h-full"
        actions={
          <Segmented
            options={[
              { value: "mouse", label: "Mouse", icon: Mouse },
              { value: "keyboard", label: "Keyboard", icon: Keyboard },
            ]}
            value={device}
            onChange={setDevice}
          />
        }
      >
        <div className="flex flex-1 flex-col justify-center">
          {device === "mouse" ? (
            <MousePicker value={profile.target_key} onChange={pick} />
          ) : (
            <KeyboardPicker value={profile.target_key} onChange={pick} />
          )}
        </div>
      </Panel>
    </Locked>
  );
}

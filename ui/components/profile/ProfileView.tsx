import { ActionPanel } from "./ActionPanel";
import { LockNotice } from "./Locked";
import { TargetPanel } from "./TargetPanel";
import { TimingPanel } from "./TimingPanel";
import type { ProfileProps } from "./types";

export function ProfileView(props: ProfileProps) {
  return (
    <div className="space-y-4">
      <LockNotice locked={props.status.locked} />
      <div className="grid grid-cols-[minmax(0,5fr)_minmax(0,7fr)] gap-4">
        <ActionPanel {...props} />
        <TargetPanel {...props} />
      </div>
      <TimingPanel {...props} />
    </div>
  );
}

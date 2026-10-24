import { useState, type FormEvent } from "react";
import { cx } from "../../lib/cx";
import { Button } from "../ui";
import { Modal } from "./Modal";

export function NameDialog({
  title,
  initial,
  confirm,
  onSubmit,
  onClose,
}: {
  title: string;
  initial: string;
  confirm: string;
  onSubmit: (name: string) => Promise<unknown>;
  onClose: () => void;
}) {
  const [value, setValue] = useState(initial);
  const [error, setError] = useState("");
  const submit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit(value.trim());
      onClose();
    } catch (err) {
      setError(String(err));
    }
  };
  return (
    <Modal title={title} description="Up to 24 characters. Each profile keeps its own settings and hotkey." onClose={onClose}>
      <form onSubmit={submit}>
        <input
          autoFocus
          aria-label="Profile name"
          value={value}
          onFocus={(e) => e.target.select()}
          onChange={(e) => {
            setValue(e.target.value);
            setError("");
          }}
          className={cx(
            "h-10 w-full rounded-lg bg-zinc-950/60 px-3 text-sm ring-1 outline-none select-text ring-inset focus:ring-2",
            error ? "ring-rose-500/70 focus:ring-rose-500" : "ring-white/10 focus:ring-violet-500",
          )}
        />
        <p className="mt-2 h-4 text-xs text-rose-400">{error}</p>
        <div className="mt-3 flex justify-end gap-2">
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="primary">
            {confirm}
          </Button>
        </div>
      </form>
    </Modal>
  );
}

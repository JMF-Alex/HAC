import { TriangleAlert } from "lucide-react";
import { Button } from "../ui";
import { Modal } from "./Modal";

export function ConfirmDialog({
  title,
  message,
  confirm = "OK",
  danger,
  onConfirm,
  onClose,
}: {
  title: string;
  message: string;
  confirm?: string;
  danger?: boolean;
  onConfirm?: () => void;
  onClose: () => void;
}) {
  return (
    <Modal title={title} description={message} icon={TriangleAlert} danger={danger} onClose={onClose}>
      <div className="mt-5 flex justify-end gap-2">
        {onConfirm && (
          <Button variant="ghost" autoFocus={danger} onClick={onClose}>
            Cancel
          </Button>
        )}
        <Button
          autoFocus={!danger}
          variant={danger ? "danger" : "primary"}
          onClick={() => {
            onConfirm?.();
            onClose();
          }}
        >
          {confirm}
        </Button>
      </div>
    </Modal>
  );
}

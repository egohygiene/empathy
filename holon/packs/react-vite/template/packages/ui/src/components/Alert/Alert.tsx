import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, ReactNode } from "react";

export type AlertTone = "danger" | "info" | "success" | "warning";

export interface AlertProps extends Omit<HTMLAttributes<HTMLDivElement>, "title"> {
  readonly actions?: ReactNode;
  readonly title?: ReactNode;
  readonly tone?: AlertTone;
}

export function Alert({
  actions,
  children,
  className,
  role,
  title,
  tone = "info",
  ...props
}: AlertProps) {
  return (
    <div
      className={cn("eh-alert", `eh-alert--${tone}`, className)}
      role={role ?? (tone === "danger" ? "alert" : "status")}
      {...props}
    >
      <div className="eh-alert__content">
        {title ? <strong className="eh-alert__title">{title}</strong> : null}
        <div className="eh-alert__message">{children}</div>
      </div>
      {actions ? <div className="eh-alert__actions">{actions}</div> : null}
    </div>
  );
}

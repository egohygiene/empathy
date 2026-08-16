import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, ReactNode } from "react";

export interface EmptyStateProps extends Omit<HTMLAttributes<HTMLDivElement>, "title"> {
  readonly actions?: ReactNode;
  readonly description?: ReactNode;
  readonly icon?: ReactNode;
  readonly title: ReactNode;
}

export function EmptyState({
  actions,
  className,
  description,
  icon,
  title,
  ...props
}: EmptyStateProps) {
  return (
    <div className={cn("eh-empty-state", className)} {...props}>
      {icon ? <div className="eh-empty-state__icon">{icon}</div> : null}
      <h2 className="eh-empty-state__title">{title}</h2>
      {description ? <div className="eh-empty-state__description">{description}</div> : null}
      {actions ? <div className="eh-empty-state__actions">{actions}</div> : null}
    </div>
  );
}

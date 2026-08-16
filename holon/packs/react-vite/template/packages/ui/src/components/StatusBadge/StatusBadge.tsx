import { cn } from "@egohygiene/utilities";
import type { PropsWithChildren } from "react";

export type StatusBadgeTone = "available" | "development" | "planned";

export interface StatusBadgeProps {
  readonly className?: string;
  readonly tone?: StatusBadgeTone;
}

export function StatusBadge({
  children,
  className,
  tone = "development",
}: PropsWithChildren<StatusBadgeProps>) {
  return <span className={cn("eh-badge", `eh-badge--${tone}`, className)}>{children}</span>;
}

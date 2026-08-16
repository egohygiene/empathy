import type { ReactNode } from "react";

export interface StatusBadgeProps {
  readonly children: ReactNode;
  readonly tone?: "neutral" | "accent" | "success";
}

export function StatusBadge({ children, tone = "neutral" }: StatusBadgeProps) {
  return <span className={`status-badge status-badge--${tone}`}>{children}</span>;
}

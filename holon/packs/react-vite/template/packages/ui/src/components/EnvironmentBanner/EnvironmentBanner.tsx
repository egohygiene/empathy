import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, ReactNode } from "react";

export type EnvironmentBannerTone = "development" | "preview" | "warning";

export interface EnvironmentBannerProps extends HTMLAttributes<HTMLElement> {
  readonly description?: ReactNode;
  readonly hidden?: boolean;
  readonly label: ReactNode;
  readonly tone?: EnvironmentBannerTone;
}

export function EnvironmentBanner({
  className,
  description,
  hidden = false,
  label,
  tone = "development",
  ...props
}: EnvironmentBannerProps) {
  if (hidden) {
    return null;
  }

  return (
    <aside
      aria-label="Environment notice"
      className={cn("eh-environment-banner", `eh-environment-banner--${tone}`, className)}
      {...props}
    >
      <strong>{label}</strong>
      {description ? <span>{description}</span> : null}
    </aside>
  );
}

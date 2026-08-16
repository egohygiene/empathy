import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, ReactNode } from "react";

import { Spinner } from "../Spinner";

export interface LoadingStateProps extends HTMLAttributes<HTMLDivElement> {
  readonly message?: ReactNode;
  readonly size?: "inline" | "page" | "section";
}

export function LoadingState({
  className,
  message = "Loading…",
  size = "section",
  ...props
}: LoadingStateProps) {
  return (
    <div
      aria-live="polite"
      className={cn("eh-loading-state", `eh-loading-state--${size}`, className)}
      role="status"
      {...props}
    >
      <Spinner decorative size={size === "page" ? "large" : "medium"} />
      <span>{message}</span>
    </div>
  );
}

import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes } from "react";

export interface SkeletonProps extends HTMLAttributes<HTMLSpanElement> {
  readonly height?: number | string;
  readonly shape?: "circle" | "line" | "rectangle";
  readonly width?: number | string;
}

export function Skeleton({
  className,
  height,
  shape = "line",
  style,
  width,
  ...props
}: SkeletonProps) {
  const dimensions = {
    ...(height === undefined ? {} : { height }),
    ...(width === undefined ? {} : { width }),
  };

  return (
    <span
      aria-hidden="true"
      className={cn("eh-skeleton", `eh-skeleton--${shape}`, className)}
      style={{ ...style, ...dimensions }}
      {...props}
    />
  );
}

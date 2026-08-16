import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes } from "react";

export interface HorizontalScrollerProps extends HTMLAttributes<HTMLDivElement> {
  readonly label: string;
}

export function HorizontalScroller({
  children,
  className,
  label,
  ...props
}: HorizontalScrollerProps) {
  return (
    <section
      aria-label={label}
      className={cn("eh-horizontal-scroller", className)}
      // biome-ignore lint/a11y/noNoninteractiveTabindex: Overflow regions require a keyboard focus target.
      tabIndex={0}
      {...props}
    >
      {children}
    </section>
  );
}

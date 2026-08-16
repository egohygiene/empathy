import type { HTMLAttributes, ReactNode } from "react";

export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  readonly children: ReactNode;
}

export function Container({ children, className, ...containerProps }: ContainerProps) {
  const classes = ["container", className].filter(Boolean).join(" ");
  return (
    <div className={classes} {...containerProps}>
      {children}
    </div>
  );
}

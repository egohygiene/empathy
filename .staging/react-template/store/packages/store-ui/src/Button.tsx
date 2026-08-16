import type { ButtonHTMLAttributes, ReactNode } from "react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  readonly children: ReactNode;
  readonly variant?: "primary" | "secondary" | "ghost";
  readonly busy?: boolean;
}

export function Button({
  children,
  variant = "primary",
  busy = false,
  disabled,
  className,
  ...buttonProps
}: ButtonProps) {
  const classes = ["button", `button--${variant}`, className].filter(Boolean).join(" ");

  return (
    <button className={classes} disabled={disabled || busy} aria-busy={busy} {...buttonProps}>
      {busy ? "working…" : children}
    </button>
  );
}

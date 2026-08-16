import { cn } from "@egohygiene/utilities";
import type { AnchorHTMLAttributes } from "react";

import { Spinner } from "../Spinner";
import type { ButtonProps } from "./Button.types";

function buttonClassName(tone: NonNullable<ButtonProps["tone"]>, disabled?: boolean) {
  return cn("eh-button", `eh-button--${tone}`, disabled && "eh-button--disabled");
}

export function Button({
  children,
  className,
  disabled,
  icon,
  loading,
  loadingLabel = "Loading",
  tone = "primary",
  ...props
}: ButtonProps) {
  return (
    <button
      aria-busy={loading || undefined}
      className={cn(buttonClassName(tone, disabled || loading), className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <Spinner decorative size="small" /> : icon}
      <span>{loading ? loadingLabel : children}</span>
    </button>
  );
}

export function LinkButton({
  className,
  href,
  tone = "secondary",
  ...props
}: AnchorHTMLAttributes<HTMLAnchorElement> & { readonly tone?: ButtonProps["tone"] }) {
  return (
    <a className={cn(buttonClassName(tone ?? "secondary"), className)} href={href} {...props} />
  );
}

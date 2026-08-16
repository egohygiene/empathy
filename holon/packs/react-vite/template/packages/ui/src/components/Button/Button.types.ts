import type { ButtonHTMLAttributes, ReactNode } from "react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  readonly icon?: ReactNode;
  readonly loading?: boolean;
  readonly loadingLabel?: string;
  readonly tone?: "primary" | "secondary" | "ghost";
}

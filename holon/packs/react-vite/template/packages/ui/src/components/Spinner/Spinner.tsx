import { cn } from "@egohygiene/utilities";

export interface SpinnerProps {
  readonly className?: string;
  readonly decorative?: boolean;
  readonly label?: string;
  readonly size?: "large" | "medium" | "small";
}

export function Spinner({
  className,
  decorative = false,
  label = "Loading",
  size = "medium",
}: SpinnerProps) {
  const spinnerClassName = cn("eh-spinner", `eh-spinner--${size}`, className);

  if (decorative) {
    return <span aria-hidden="true" className={spinnerClassName} />;
  }

  return (
    <span aria-label={label} className={spinnerClassName} role="status">
      <span className="eh-visually-hidden">{label}</span>
    </span>
  );
}

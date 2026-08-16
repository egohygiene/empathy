import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, PropsWithChildren } from "react";

export function Container({
  children,
  className,
}: PropsWithChildren<{ readonly className?: string }>) {
  return <div className={cn("eh-container", className)}>{children}</div>;
}

export function Stack({ children, className }: PropsWithChildren<{ readonly className?: string }>) {
  return <div className={cn("eh-stack", className)}>{children}</div>;
}

export function Cluster({
  children,
  className,
}: PropsWithChildren<{ readonly className?: string }>) {
  return <div className={cn("eh-cluster", className)}>{children}</div>;
}

export function Card({ children, className }: PropsWithChildren<{ readonly className?: string }>) {
  return <article className={cn("eh-card", className)}>{children}</article>;
}

export function PageSection({
  children,
  className,
  ...props
}: PropsWithChildren<HTMLAttributes<HTMLElement>>) {
  return (
    <section className={cn("eh-section", className)} {...props}>
      {children}
    </section>
  );
}

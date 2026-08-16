import { cn } from "@egohygiene/utilities";
import type { HTMLAttributes, ReactNode } from "react";

export interface MediaCardProps extends Omit<HTMLAttributes<HTMLElement>, "title"> {
  readonly actions?: ReactNode;
  readonly description?: ReactNode;
  readonly href?: string;
  readonly imageAlt: string;
  readonly imageSrc: string;
  readonly title: ReactNode;
}

export function MediaCard({
  actions,
  className,
  description,
  href,
  imageAlt,
  imageSrc,
  title,
  ...props
}: MediaCardProps) {
  const heading = href ? (
    <a className="eh-media-card__link" href={href}>
      {title}
    </a>
  ) : (
    title
  );

  return (
    <article className={cn("eh-media-card", className)} {...props}>
      <img alt={imageAlt} className="eh-media-card__image" loading="lazy" src={imageSrc} />
      <div className="eh-media-card__body">
        <h3 className="eh-media-card__title">{heading}</h3>
        {description ? <div className="eh-media-card__description">{description}</div> : null}
        {actions ? <div className="eh-media-card__actions">{actions}</div> : null}
      </div>
    </article>
  );
}

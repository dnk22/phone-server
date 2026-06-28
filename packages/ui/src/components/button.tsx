import type { ButtonHTMLAttributes } from 'react';

import { cn } from '../lib/cn';

type ButtonVariant = 'default' | 'secondary' | 'ghost' | 'outline' | 'destructive';

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
};

const variants: Record<ButtonVariant, string> = {
  default: 'bg-primary text-primary-foreground hover:opacity-90',
  secondary: 'bg-secondary text-secondary-foreground hover:opacity-90',
  ghost: 'hover:bg-accent hover:text-accent-foreground',
  outline: 'border border-border bg-background hover:bg-accent',
  destructive: 'bg-destructive text-primary-foreground hover:opacity-90',
};

export function Button({ className, variant = 'default', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex min-h-10 items-center justify-center rounded-md px-4 py-2 text-sm font-medium focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring disabled:pointer-events-none disabled:opacity-50',
        variants[variant],
        className,
      )}
      {...props}
    />
  );
}

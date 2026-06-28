import type { HTMLAttributes, ReactNode } from 'react';

import { cn } from '../lib/cn';

export function Badge({ className, ...props }: HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full bg-secondary px-2.5 py-1 text-xs font-medium text-secondary-foreground',
        className,
      )}
      {...props}
    />
  );
}

export function Separator({ className, ...props }: HTMLAttributes<HTMLHRElement>) {
  return <hr className={cn('border-border', className)} {...props} />;
}

export function Skeleton({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('animate-pulse rounded-md bg-muted', className)} {...props} />;
}

export function Progress({ className, value = 0 }: { className?: string; value?: number }) {
  const width = `${Math.max(0, Math.min(value, 100))}%`;
  return (
    <div
      aria-valuemax={100}
      aria-valuemin={0}
      aria-valuenow={value}
      className={cn('h-2 overflow-hidden rounded-full bg-muted', className)}
      role="progressbar"
    >
      <div className="h-full bg-primary" style={{ width }} />
    </div>
  );
}

export function Avatar({ fallback, className }: { fallback: ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        'inline-flex size-9 items-center justify-center rounded-full bg-muted text-sm font-medium',
        className,
      )}
    >
      {fallback}
    </span>
  );
}

export function Tooltip({ children }: { children: ReactNode }) {
  return <>{children}</>;
}

export function DropdownMenu({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}

export function Sheet({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}

export function Sidebar({ className, ...props }: HTMLAttributes<HTMLElement>) {
  return <aside className={cn('border-r border-border bg-card', className)} {...props} />;
}

export function Breadcrumb({ className, ...props }: HTMLAttributes<HTMLElement>) {
  return <nav aria-label="Breadcrumb" className={className} {...props} />;
}

export function Command({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('rounded-md border border-border bg-popover', className)} {...props} />;
}

export function Dialog({ children }: { children: ReactNode }) {
  return <div role="dialog">{children}</div>;
}

export function AlertDialog({ children }: { children: ReactNode }) {
  return <div role="alertdialog">{children}</div>;
}

export function Tabs({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('space-y-4', className)} {...props} />;
}

export function Select({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('rounded-md border border-input bg-background px-3 py-2', className)}
      {...props}
    />
  );
}

export function Switch({ checked, label }: { checked?: boolean; label: string }) {
  return (
    <span
      aria-checked={checked ?? false}
      aria-label={label}
      className="inline-flex h-6 w-10 rounded-full bg-muted"
      role="switch"
    />
  );
}

export function ScrollArea({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('overflow-auto', className)} {...props} />;
}

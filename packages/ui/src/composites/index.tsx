import { AlertTriangle } from 'lucide-react';
import type { ReactNode } from 'react';
import { Toaster } from 'sonner';

import { Button } from '../components/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/card';
import { Badge, Progress } from '../components/primitives';

export function PageHeader({
  title,
  description,
  actions,
}: {
  title: string;
  description?: string;
  actions?: ReactNode;
}) {
  return (
    <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        {description ? <p className="mt-2 max-w-3xl text-muted-foreground">{description}</p> : null}
      </div>
      {actions ? <div>{actions}</div> : null}
    </header>
  );
}

export function StatusBadge({
  status,
}: {
  status: 'success' | 'warning' | 'error' | 'info' | 'neutral';
}) {
  return <Badge data-status={status}>{status}</Badge>;
}

export function FeatureLock({ reason = 'Upgrade required' }: { reason?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
      <AlertTriangle aria-hidden size={16} />
      {reason}
    </span>
  );
}

export function UpgradePrompt({
  message = 'Upgrade to unlock this feature.',
}: {
  message?: string;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Upgrade required</CardTitle>
      </CardHeader>
      <CardContent>{message}</CardContent>
    </Card>
  );
}

export function UsageMeter({ label, value }: { label: string; value: number }) {
  return (
    <div className="space-y-2">
      <span className="text-sm font-medium">{label}</span>
      <Progress value={value} />
    </div>
  );
}

export function EmptyState({ title, description }: { title: string; description?: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      {description ? <CardContent>{description}</CardContent> : null}
    </Card>
  );
}

export function ErrorState({
  title = 'Something went wrong',
  description,
}: {
  title?: string;
  description?: string;
}) {
  return description ? (
    <EmptyState description={description} title={title} />
  ) : (
    <EmptyState title={title} />
  );
}

export function LoadingState({ label = 'Loading' }: { label?: string }) {
  return (
    <p aria-live="polite" className="text-sm text-muted-foreground">
      {label}…
    </p>
  );
}

export function ConfirmDialog({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div aria-label={title} role="alertdialog">
      {children}
    </div>
  );
}

export function SectionCard({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

export { Button, Toaster };

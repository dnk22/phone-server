import { PageHeader, SectionCard } from '@repo/ui';

export function NotFoundPage() {
  return (
    <div className="space-y-6">
      <PageHeader description="The route you requested does not exist." title="Page not found" />
      <SectionCard title="404">Use the navigation to return to a known route.</SectionCard>
    </div>
  );
}

export default NotFoundPage;

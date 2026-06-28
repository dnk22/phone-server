import { PageHeader, SectionCard } from '@repo/ui';

export function ForbiddenPage() {
  return (
    <div className="space-y-6">
      <PageHeader description="You do not have permission to access this area." title="Forbidden" />
      <SectionCard title="Access model">
        Role/permission controls actions. Feature entitlement controls purchased access. Menu
        visibility is not a security boundary.
      </SectionCard>
    </div>
  );
}

export default ForbiddenPage;

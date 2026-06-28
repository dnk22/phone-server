import { PageHeader, SectionCard } from '@repo/ui';

export function PagePlaceholder({
  description,
  sections = ['Foundation placeholder'],
  title,
}: {
  title: string;
  description: string;
  sections?: string[];
}) {
  return (
    <div className="space-y-6">
      <PageHeader description={description} title={title} />
      <div className="grid gap-4 md:grid-cols-2">
        {sections.map((section) => (
          <SectionCard key={section} title={section}>
            This area will be implemented later.
          </SectionCard>
        ))}
      </div>
    </div>
  );
}

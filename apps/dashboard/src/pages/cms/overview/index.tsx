import { PagePlaceholder } from '../../page-placeholder';

export default function CmsOverviewPage() {
  return (
    <PagePlaceholder
      description="CMS overview foundation."
      sections={[
        'Current plan',
        'Available features',
        'Usage',
        'Automation devices',
        'Recent activity',
      ]}
      title="Overview"
    />
  );
}

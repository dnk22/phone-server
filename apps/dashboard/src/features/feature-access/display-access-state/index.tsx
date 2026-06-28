import { FeatureLock, StatusBadge } from '@repo/ui';

import type { FeatureAccess } from '../../../entities/feature-access/model';

export function DisplayAccessState({ access }: { access: FeatureAccess }) {
  if (!access.available) {
    return <FeatureLock reason={access.reason ?? 'Feature unavailable'} />;
  }

  return <StatusBadge status={access.entitled ? 'success' : 'warning'} />;
}

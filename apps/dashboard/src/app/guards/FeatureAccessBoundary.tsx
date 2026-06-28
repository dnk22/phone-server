import { UpgradePrompt } from '@repo/ui';
import type { ReactNode } from 'react';

import { resolveFeatureAccess } from '../../features/feature-access/resolve-access';

export function FeatureAccessBoundary({
  children,
  featureCode,
  mode = 'block',
}: {
  children: ReactNode;
  featureCode: string;
  mode?: 'block' | 'freemium';
}) {
  const access = resolveFeatureAccess(
    featureCode,
    mode === 'freemium' ? 'anonymous' : 'authenticated',
  );

  if (!access.available && mode === 'block') {
    return <UpgradePrompt message={access.reason ?? 'This feature is locked.'} />;
  }

  return <>{children}</>;
}

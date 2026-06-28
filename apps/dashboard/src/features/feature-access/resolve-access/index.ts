import type { FeatureAccess, FeatureTier } from '../../../entities/feature-access/model';

export function resolveFeatureAccess(
  featureCode: string,
  tier: FeatureTier = 'anonymous',
): FeatureAccess {
  return {
    available: tier === 'anonymous' || tier === 'authenticated',
    entitled: tier !== 'paid',
    featureCode,
    limits: { daily: 3 },
    lockedCapabilities: tier === 'anonymous' ? ['history', 'batch', 'quality'] : [],
    tier,
    usage: { daily: 0 },
  };
}

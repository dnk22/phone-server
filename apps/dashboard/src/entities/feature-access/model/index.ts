export type FeatureTier = 'anonymous' | 'authenticated' | 'paid' | 'admin';

export type FeatureAccess = {
  featureCode: string;
  available: boolean;
  tier: FeatureTier;
  entitled: boolean;
  limits: Record<string, unknown>;
  usage: Record<string, number>;
  lockedCapabilities: string[];
  reason?: string;
};

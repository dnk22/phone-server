import type { User } from '../../user/model';

export type AuthState = 'loading' | 'authenticated' | 'unauthenticated' | 'expired';

export type Session = {
  user: User;
  roles: string[];
  permissions: string[];
  entitlements: string[];
};

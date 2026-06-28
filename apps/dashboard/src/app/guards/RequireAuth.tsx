import { LoadingState } from '@repo/ui';
import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router';

import { useSession } from '../../features/auth/restore-session/session-context';
import { routePaths } from '../router/route-paths';

export function RequireAuth({ children }: { children: ReactNode }) {
  const { state } = useSession();
  const location = useLocation();

  if (state === 'loading') {
    return <LoadingState label="Restoring session" />;
  }

  if (state === 'unauthenticated' || state === 'expired') {
    return <Navigate replace state={{ redirectTo: location.pathname }} to={routePaths.login} />;
  }

  return <>{children}</>;
}

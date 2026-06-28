import type { ReactNode } from 'react';

import { useSession } from '../../features/auth/restore-session/session-context';
import { ForbiddenPage } from '../../pages/errors/ForbiddenPage';

export function RequirePermission({
  children,
  permission,
}: {
  children: ReactNode;
  permission: string;
}) {
  const { session } = useSession();

  if (!session?.permissions.includes(permission)) {
    return <ForbiddenPage />;
  }

  return <>{children}</>;
}

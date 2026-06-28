import type { ReactNode } from 'react';

import { RequirePermission } from './RequirePermission';

export function AdminRoute({ children, permission }: { children: ReactNode; permission: string }) {
  return <RequirePermission permission={permission}>{children}</RequirePermission>;
}

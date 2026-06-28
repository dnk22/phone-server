import type { ReactNode } from 'react';
import { createContext, useContext, useMemo } from 'react';

import type { AuthState, Session } from '../../../entities/session/model';

type SessionContextValue = {
  state: AuthState;
  session: Session | null;
  login: () => void;
  logout: () => void;
};

export const mockSession: Session = {
  entitlements: ['automation.basic'],
  permissions: ['cms.read', 'automation.read'],
  roles: ['member'],
  user: {
    email: 'demo@example.com',
    id: 'demo-user',
    name: 'Demo User',
  },
};

const SessionContext = createContext<SessionContextValue | null>(null);

export function SessionProvider({
  children,
  initialState = 'unauthenticated',
  initialSession = null,
}: {
  children: ReactNode;
  initialState?: AuthState;
  initialSession?: Session | null;
}) {
  const value = useMemo<SessionContextValue>(
    () => ({
      login: () => undefined,
      logout: () => undefined,
      session: initialSession,
      state: initialState,
    }),
    [initialSession, initialState],
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession() {
  const value = useContext(SessionContext);
  if (!value) {
    throw new Error('useSession must be used within SessionProvider');
  }
  return value;
}

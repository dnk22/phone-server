import type { ReactNode } from 'react';
import { useEffect } from 'react';

import { env } from '../config/env';

export function MockApiProvider({ children }: { children: ReactNode }) {
  useEffect(() => {
    if (!env.isDevelopment || !env.enableMockApi) {
      return;
    }

    void import('../../shared/api/mock/browser').then(({ worker }) => {
      void worker.start({ onUnhandledRequest: 'bypass' });
    });
  }, []);

  return <>{children}</>;
}

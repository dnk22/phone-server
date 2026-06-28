import { Toaster } from '@repo/ui';
import type { ReactNode } from 'react';

import { SessionProvider } from '../../features/auth/restore-session/session-context';
import { MockApiProvider } from './MockApiProvider';
import { QueryProvider } from './QueryProvider';
import { ThemeProvider } from './ThemeProvider';
import { TooltipProvider } from './TooltipProvider';

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <QueryProvider>
      <SessionProvider>
        <ThemeProvider>
          <TooltipProvider>
            <MockApiProvider>
              {children}
              <Toaster richColors />
            </MockApiProvider>
          </TooltipProvider>
        </ThemeProvider>
      </SessionProvider>
    </QueryProvider>
  );
}

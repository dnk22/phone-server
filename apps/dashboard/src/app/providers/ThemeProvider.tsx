import type { ReactNode } from 'react';
import { useEffect } from 'react';

import { useUiStore } from '../../shared/stores/ui-store';

export function ThemeProvider({ children }: { children: ReactNode }) {
  const theme = useUiStore((state) => state.themePreference);

  useEffect(() => {
    document.documentElement.classList.toggle('light', theme === 'light');
  }, [theme]);

  return <>{children}</>;
}

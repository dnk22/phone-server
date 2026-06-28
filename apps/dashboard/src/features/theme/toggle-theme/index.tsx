import { Button } from '@repo/ui';
import { Moon, Sun } from 'lucide-react';

import { useUiStore } from '../../../shared/stores/ui-store';

export function ToggleTheme() {
  const theme = useUiStore((state) => state.themePreference);
  const toggleTheme = useUiStore((state) => state.toggleTheme);

  return (
    <Button aria-label="Toggle theme" onClick={toggleTheme} type="button" variant="ghost">
      {theme === 'dark' ? <Sun aria-hidden size={18} /> : <Moon aria-hidden size={18} />}
    </Button>
  );
}

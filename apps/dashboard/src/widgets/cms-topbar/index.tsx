import { Button } from '@repo/ui';
import { Menu } from 'lucide-react';

import { ToggleTheme } from '../../features/theme/toggle-theme';
import { useUiStore } from '../../shared/stores/ui-store';
import { UserMenu } from '../user-menu';

export function CmsTopbar() {
  const setMobileSidebarOpen = useUiStore((state) => state.setMobileSidebarOpen);

  return (
    <header className="flex min-h-16 items-center justify-between border-b border-border bg-background px-4">
      <Button
        aria-label="Open mobile sidebar"
        className="md:hidden"
        onClick={() => setMobileSidebarOpen(true)}
        type="button"
        variant="ghost"
      >
        <Menu aria-hidden size={20} />
      </Button>
      <p className="text-sm text-muted-foreground">Control plane dashboard</p>
      <div className="flex items-center gap-2">
        <ToggleTheme />
        <UserMenu />
      </div>
    </header>
  );
}

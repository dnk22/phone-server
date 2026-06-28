import { Avatar, Button } from '@repo/ui';

import { useSession } from '../../features/auth/restore-session/session-context';

export function UserMenu() {
  const { logout, session } = useSession();
  const initials = session?.user.name.slice(0, 1).toUpperCase() ?? 'G';

  return (
    <div className="flex items-center gap-3">
      <Avatar fallback={initials} />
      <Button aria-label="Logout" onClick={logout} type="button" variant="ghost">
        Logout
      </Button>
    </div>
  );
}

import { Button } from '@repo/ui';
import { Link } from 'react-router';

import { publicNavigation } from '../../app/config/navigation';
import { routePaths } from '../../app/router/route-paths';
import { useSession } from '../../features/auth/restore-session/session-context';

export function PublicHeader() {
  const { state } = useSession();
  const authenticated = state === 'authenticated';

  return (
    <header className="border-b border-border bg-background">
      <nav
        className="mx-auto flex min-h-16 max-w-6xl items-center justify-between px-4"
        aria-label="Public"
      >
        <Link className="font-semibold" to={routePaths.landing}>
          Android Linux Server
        </Link>
        <div className="hidden items-center gap-4 md:flex">
          {publicNavigation.map((item) => (
            <Link
              className="text-sm text-muted-foreground hover:text-foreground"
              key={item.code}
              to={item.path ?? routePaths.landing}
            >
              {item.label}
            </Link>
          ))}
          {authenticated ? (
            <Link to={routePaths.cmsOverview}>
              <Button type="button">Dashboard</Button>
            </Link>
          ) : (
            <>
              <Link className="text-sm" to={routePaths.login}>
                Login
              </Link>
              <Link className="text-sm" to={routePaths.register}>
                Register
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

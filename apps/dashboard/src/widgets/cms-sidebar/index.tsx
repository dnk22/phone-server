import { Link } from 'react-router';

import { cmsNavigation } from '../../app/config/navigation';
import { useSession } from '../../features/auth/restore-session/session-context';
import { buildNavigation } from '../../features/navigation/build-navigation';

export function CmsSidebar() {
  const { session } = useSession();
  const items = buildNavigation(cmsNavigation, session?.permissions ?? []);

  return (
    <aside
      className="hidden w-72 shrink-0 border-r border-border bg-card p-4 md:block"
      aria-label="CMS sidebar"
    >
      <p className="mb-4 text-sm font-semibold">CMS</p>
      <nav className="space-y-4">
        {items.map((item) => (
          <div key={item.code}>
            {item.path ? (
              <Link className="text-sm font-medium" to={item.path}>
                {item.label}
              </Link>
            ) : (
              <p className="text-sm font-medium">{item.label}</p>
            )}
            {item.children ? (
              <div className="mt-2 grid gap-1 pl-3">
                {item.children.map((child) => (
                  <Link
                    className="text-sm text-muted-foreground hover:text-foreground"
                    key={child.code}
                    to={child.path ?? '#'}
                  >
                    {child.label}
                  </Link>
                ))}
              </div>
            ) : null}
          </div>
        ))}
      </nav>
    </aside>
  );
}

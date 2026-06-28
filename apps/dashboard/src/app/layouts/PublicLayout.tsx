import { Outlet } from 'react-router';

import { PublicFooter } from '../../widgets/public-footer';
import { PublicHeader } from '../../widgets/public-header';

export function PublicLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <PublicHeader />
      <main className="mx-auto max-w-6xl px-4 py-10">
        <Outlet />
      </main>
      <PublicFooter />
    </div>
  );
}

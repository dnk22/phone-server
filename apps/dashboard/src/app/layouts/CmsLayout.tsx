import { Outlet } from 'react-router';

import { CmsBreadcrumb } from '../../widgets/cms-breadcrumb';
import { CmsSidebar } from '../../widgets/cms-sidebar';
import { CmsTopbar } from '../../widgets/cms-topbar';

export function CmsLayout() {
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      <CmsSidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <CmsTopbar />
        <main className="flex-1 space-y-6 p-6">
          <CmsBreadcrumb />
          <Outlet />
        </main>
      </div>
    </div>
  );
}

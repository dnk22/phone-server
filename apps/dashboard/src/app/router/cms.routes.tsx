import { LoadingState } from '@repo/ui';
import { lazy, Suspense } from 'react';
import { Navigate, type RouteObject } from 'react-router';

import { RequireAuth } from '../guards/RequireAuth';
import { CmsLayout } from '../layouts/CmsLayout';
import { adminRoutes } from './admin.routes';
import { routePaths } from './route-paths';

const CmsOverviewPage = lazy(() => import('../../pages/cms/overview'));
const AutomationDevicesPage = lazy(() => import('../../pages/cms/automation/devices'));
const AutomationScenariosPage = lazy(() => import('../../pages/cms/automation/scenarios'));
const AutomationExecutionsPage = lazy(() => import('../../pages/cms/automation/executions'));
const AutomationLogsPage = lazy(() => import('../../pages/cms/automation/logs'));
const MediaHistoryPage = lazy(() => import('../../pages/cms/media/history'));
const UsagePage = lazy(() => import('../../pages/cms/usage'));
const BillingPage = lazy(() => import('../../pages/cms/billing'));
const AccountPage = lazy(() => import('../../pages/cms/account'));
const SettingsPage = lazy(() => import('../../pages/cms/settings'));

function withSuspense(element: React.ReactNode) {
  return <Suspense fallback={<LoadingState />}>{element}</Suspense>;
}

export const cmsRoutes: RouteObject = {
  children: [
    { element: <Navigate replace to={routePaths.cmsOverview} />, index: true },
    { element: withSuspense(<CmsOverviewPage />), path: 'overview' },
    {
      children: [
        { element: withSuspense(<AutomationDevicesPage />), path: 'devices' },
        { element: withSuspense(<AutomationScenariosPage />), path: 'scenarios' },
        { element: withSuspense(<AutomationExecutionsPage />), path: 'executions' },
        { element: withSuspense(<AutomationLogsPage />), path: 'logs' },
      ],
      path: 'automation',
    },
    {
      children: [{ element: withSuspense(<MediaHistoryPage />), path: 'history' }],
      path: 'media',
    },
    { element: withSuspense(<UsagePage />), path: 'usage' },
    { element: withSuspense(<BillingPage />), path: 'billing' },
    { element: withSuspense(<AccountPage />), path: 'account' },
    { element: withSuspense(<SettingsPage />), path: 'settings' },
    adminRoutes,
  ],
  element: (
    <RequireAuth>
      <CmsLayout />
    </RequireAuth>
  ),
  path: 'cms',
};

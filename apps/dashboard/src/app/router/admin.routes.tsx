import { LoadingState } from '@repo/ui';
import { lazy, Suspense } from 'react';
import type { RouteObject } from 'react-router';

import { AdminRoute } from '../guards/AdminRoute';

const UsersPage = lazy(() => import('../../pages/cms/admin/users'));
const RolesPage = lazy(() => import('../../pages/cms/admin/roles'));
const PermissionsPage = lazy(() => import('../../pages/cms/admin/permissions'));
const FeaturesPage = lazy(() => import('../../pages/cms/admin/features'));
const PlansPage = lazy(() => import('../../pages/cms/admin/plans'));
const SubscriptionsPage = lazy(() => import('../../pages/cms/admin/subscriptions'));
const EntitlementsPage = lazy(() => import('../../pages/cms/admin/entitlements'));
const MenusPage = lazy(() => import('../../pages/cms/admin/menus'));

function withAdminPermission(element: React.ReactNode, permission: string) {
  return (
    <Suspense fallback={<LoadingState />}>
      <AdminRoute permission={permission}>{element}</AdminRoute>
    </Suspense>
  );
}

export const adminRoutes: RouteObject = {
  children: [
    { element: withAdminPermission(<UsersPage />, 'admin.users.read'), path: 'users' },
    { element: withAdminPermission(<RolesPage />, 'admin.roles.read'), path: 'roles' },
    {
      element: withAdminPermission(<PermissionsPage />, 'admin.permissions.read'),
      path: 'permissions',
    },
    { element: withAdminPermission(<FeaturesPage />, 'admin.features.read'), path: 'features' },
    { element: withAdminPermission(<PlansPage />, 'admin.plans.read'), path: 'plans' },
    {
      element: withAdminPermission(<SubscriptionsPage />, 'admin.subscriptions.read'),
      path: 'subscriptions',
    },
    {
      element: withAdminPermission(<EntitlementsPage />, 'admin.entitlements.read'),
      path: 'entitlements',
    },
    { element: withAdminPermission(<MenusPage />, 'admin.menus.read'), path: 'menus' },
  ],
  path: 'admin',
};

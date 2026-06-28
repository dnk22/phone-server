import { type RoutePath, routePaths } from './route-paths';

export type RouteRegistryItem = {
  code: string;
  path: RoutePath;
  requiredPermission?: string;
};

export const routeRegistry = {
  account: { code: 'account', path: routePaths.account },
  adminEntitlements: {
    code: 'admin.entitlements',
    path: routePaths.adminEntitlements,
    requiredPermission: 'admin.entitlements.read',
  },
  adminFeatures: {
    code: 'admin.features',
    path: routePaths.adminFeatures,
    requiredPermission: 'admin.features.read',
  },
  adminMenus: {
    code: 'admin.menus',
    path: routePaths.adminMenus,
    requiredPermission: 'admin.menus.read',
  },
  adminPermissions: {
    code: 'admin.permissions',
    path: routePaths.adminPermissions,
    requiredPermission: 'admin.permissions.read',
  },
  adminPlans: {
    code: 'admin.plans',
    path: routePaths.adminPlans,
    requiredPermission: 'admin.plans.read',
  },
  adminRoles: {
    code: 'admin.roles',
    path: routePaths.adminRoles,
    requiredPermission: 'admin.roles.read',
  },
  adminSubscriptions: {
    code: 'admin.subscriptions',
    path: routePaths.adminSubscriptions,
    requiredPermission: 'admin.subscriptions.read',
  },
  adminUsers: {
    code: 'admin.users',
    path: routePaths.adminUsers,
    requiredPermission: 'admin.users.read',
  },
  automationDevices: { code: 'automation.devices', path: routePaths.automationDevices },
  automationExecutions: { code: 'automation.executions', path: routePaths.automationExecutions },
  automationLogs: { code: 'automation.logs', path: routePaths.automationLogs },
  automationScenarios: { code: 'automation.scenarios', path: routePaths.automationScenarios },
  billing: { code: 'billing', path: routePaths.billing },
  cmsOverview: { code: 'overview', path: routePaths.cmsOverview },
  mediaHistory: { code: 'media.history', path: routePaths.mediaHistory },
  settings: { code: 'settings', path: routePaths.settings },
  usage: { code: 'usage', path: routePaths.usage },
} satisfies Record<string, RouteRegistryItem>;

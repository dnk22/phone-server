import type { NavigationItem } from '../../entities/menu/model';
import { routePaths } from '../router/route-paths';

export const publicNavigation: NavigationItem[] = [
  { code: 'home', label: 'Home', path: routePaths.landing, scope: 'public' },
  {
    code: 'video-downloader',
    featureCode: 'video.downloader',
    label: 'Video Downloader',
    path: routePaths.videoDownloader,
    scope: 'public',
  },
  { code: 'features', label: 'Features', path: routePaths.landing, scope: 'public' },
  { code: 'pricing', label: 'Pricing', path: routePaths.landing, scope: 'public' },
];

export const cmsNavigation: NavigationItem[] = [
  { code: 'overview', label: 'Overview', path: routePaths.cmsOverview, scope: 'cms' },
  {
    children: [
      {
        code: 'automation.devices',
        label: 'Devices',
        path: routePaths.automationDevices,
        scope: 'cms',
      },
      {
        code: 'automation.scenarios',
        label: 'Scenarios',
        path: routePaths.automationScenarios,
        scope: 'cms',
      },
      {
        code: 'automation.executions',
        label: 'Executions',
        path: routePaths.automationExecutions,
        scope: 'cms',
      },
      { code: 'automation.logs', label: 'Logs', path: routePaths.automationLogs, scope: 'cms' },
    ],
    code: 'automation',
    label: 'Automation',
    scope: 'cms',
  },
  {
    children: [
      { code: 'media.history', label: 'History', path: routePaths.mediaHistory, scope: 'cms' },
    ],
    code: 'media',
    label: 'Media',
    scope: 'cms',
  },
  { code: 'usage', label: 'Usage', path: routePaths.usage, scope: 'cms' },
  { code: 'billing', label: 'Billing', path: routePaths.billing, scope: 'cms' },
  { code: 'account', label: 'Account', path: routePaths.account, scope: 'cms' },
  { code: 'settings', label: 'Settings', path: routePaths.settings, scope: 'cms' },
  {
    children: [
      {
        code: 'admin.users',
        label: 'Users',
        path: routePaths.adminUsers,
        requiredPermission: 'admin.users.read',
        scope: 'admin',
      },
      {
        code: 'admin.roles',
        label: 'Roles',
        path: routePaths.adminRoles,
        requiredPermission: 'admin.roles.read',
        scope: 'admin',
      },
      {
        code: 'admin.permissions',
        label: 'Permissions',
        path: routePaths.adminPermissions,
        requiredPermission: 'admin.permissions.read',
        scope: 'admin',
      },
      {
        code: 'admin.features',
        label: 'Features',
        path: routePaths.adminFeatures,
        requiredPermission: 'admin.features.read',
        scope: 'admin',
      },
      {
        code: 'admin.plans',
        label: 'Plans',
        path: routePaths.adminPlans,
        requiredPermission: 'admin.plans.read',
        scope: 'admin',
      },
      {
        code: 'admin.subscriptions',
        label: 'Subscriptions',
        path: routePaths.adminSubscriptions,
        requiredPermission: 'admin.subscriptions.read',
        scope: 'admin',
      },
      {
        code: 'admin.entitlements',
        label: 'Entitlements',
        path: routePaths.adminEntitlements,
        requiredPermission: 'admin.entitlements.read',
        scope: 'admin',
      },
      {
        code: 'admin.menus',
        label: 'Menus',
        path: routePaths.adminMenus,
        requiredPermission: 'admin.menus.read',
        scope: 'admin',
      },
    ],
    code: 'admin',
    label: 'Admin',
    requiredPermission: 'admin.access',
    scope: 'admin',
  },
];

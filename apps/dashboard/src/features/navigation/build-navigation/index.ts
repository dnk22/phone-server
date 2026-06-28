import { routeRegistry } from '../../../app/router/route-registry';
import type { NavigationItem } from '../../../entities/menu/model';

export function buildNavigation(items: NavigationItem[], permissions: string[] = []) {
  const routeCodes = new Set(Object.values(routeRegistry).map((item) => item.code));

  return items.flatMap((item): NavigationItem[] => {
    const children = item.children ? buildNavigation(item.children, permissions) : undefined;
    const hasPath = item.path ? routeCodes.has(item.code) || item.scope === 'public' : true;
    const allowed = !item.requiredPermission || permissions.includes(item.requiredPermission);

    if (!hasPath) {
      if (import.meta.env.DEV) {
        console.warn(`Navigation item "${item.code}" does not exist in route registry.`);
      }
      return [];
    }

    if (!allowed && item.scope === 'admin') {
      return [];
    }

    if (children) {
      return [{ ...item, children }];
    }

    return [{ ...item }];
  });
}

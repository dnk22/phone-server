export type MenuScope = 'public' | 'cms' | 'admin';

export type NavigationItem = {
  code: string;
  label: string;
  path?: string;
  icon?: string;
  scope: MenuScope;
  featureCode?: string;
  requiredPermission?: string;
  locked?: boolean;
  children?: NavigationItem[];
};

import { useLocation } from 'react-router';

export function CmsBreadcrumb() {
  const location = useLocation();
  const parts = location.pathname.split('/').filter(Boolean);

  return (
    <nav aria-label="Breadcrumb" className="text-sm text-muted-foreground">
      {parts.length ? parts.join(' / ') : 'cms'}
    </nav>
  );
}

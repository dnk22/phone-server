import { ErrorState } from '@repo/ui';
import { isRouteErrorResponse, useRouteError } from 'react-router';

export function RouteErrorPage() {
  const error = useRouteError();
  const description = isRouteErrorResponse(error) ? error.statusText : 'Route rendering failed.';

  return <ErrorState description={description} title="Route error" />;
}

export default RouteErrorPage;

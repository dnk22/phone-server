import { RouterProvider as ReactRouterProvider } from 'react-router';

import { router } from '../router/router';

export function RouterProvider() {
  return <ReactRouterProvider router={router} />;
}

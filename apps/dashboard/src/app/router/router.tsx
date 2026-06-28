import { createBrowserRouter, createMemoryRouter } from 'react-router';

import NotFoundPage from '../../pages/errors/NotFoundPage';
import RouteErrorPage from '../../pages/errors/RouteErrorPage';
import { authRoutes } from './auth.routes';
import { cmsRoutes } from './cms.routes';
import { publicRoutes } from './public.routes';

export const appRoutes = [
  {
    children: [publicRoutes, authRoutes, cmsRoutes, { element: <NotFoundPage />, path: '*' }],
    errorElement: <RouteErrorPage />,
    path: '/',
  },
];

export const router = createBrowserRouter(appRoutes);

export function createTestRouter(initialEntries: string[] = ['/']) {
  return createMemoryRouter(appRoutes, { initialEntries });
}

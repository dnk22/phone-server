import { render, screen } from '@testing-library/react';
import type { ReactNode } from 'react';
import { createMemoryRouter, RouterProvider } from 'react-router';
import { describe, expect, it } from 'vitest';

import { RequireAuth } from './app/guards/RequireAuth';
import { RequirePermission } from './app/guards/RequirePermission';
import { AuthLayout } from './app/layouts/AuthLayout';
import { CmsLayout } from './app/layouts/CmsLayout';
import { PublicLayout } from './app/layouts/PublicLayout';
import { AppProviders } from './app/providers/AppProviders';
import { ThemeProvider } from './app/providers/ThemeProvider';
import { appRoutes } from './app/router/router';
import { mockSession, SessionProvider } from './features/auth/restore-session/session-context';
import { useUiStore } from './shared/stores/ui-store';

function renderRoute(path: string) {
  const router = createMemoryRouter(appRoutes, { initialEntries: [path] });

  render(
    <AppProviders>
      <RouterProvider router={router} />
    </AppProviders>,
  );
}

function renderWithSession(children: ReactNode, session = mockSession) {
  render(
    <SessionProvider
      initialSession={session}
      initialState={session ? 'authenticated' : 'unauthenticated'}
    >
      {children}
    </SessionProvider>,
  );
}

describe('routing foundation', () => {
  it('renders the landing page at /', async () => {
    renderRoute('/');

    expect(
      await screen.findByRole('heading', { name: 'Android Linux Server' }),
    ).toBeInTheDocument();
  });

  it('renders video downloader without auth', async () => {
    renderRoute('/video-downloader');

    expect(await screen.findByRole('heading', { name: 'Video Downloader' })).toBeInTheDocument();
  });

  it('protects /cms/overview', async () => {
    renderRoute('/cms/overview');

    expect(await screen.findByRole('heading', { name: 'Login' })).toBeInTheDocument();
  });

  it('renders 404 for unknown routes', async () => {
    renderRoute('/missing');

    expect(await screen.findByRole('heading', { name: 'Page not found' })).toBeInTheDocument();
  });
});

describe('guards', () => {
  it('RequireAuth allows authenticated state', () => {
    const router = createMemoryRouter(
      [
        {
          element: (
            <SessionProvider initialSession={mockSession} initialState="authenticated">
              <RequireAuth>
                <p>Private content</p>
              </RequireAuth>
            </SessionProvider>
          ),
          path: '/',
        },
      ],
      { initialEntries: ['/'] },
    );

    render(<RouterProvider router={router} />);

    expect(screen.getByText('Private content')).toBeInTheDocument();
  });

  it('RequireAuth redirects unauthenticated state', () => {
    const router = createMemoryRouter(
      [
        {
          element: (
            <SessionProvider initialSession={null} initialState="unauthenticated">
              <RequireAuth>
                <p>Private content</p>
              </RequireAuth>
            </SessionProvider>
          ),
          path: '/private',
        },
        { element: <p>Login target</p>, path: '/login' },
      ],
      { initialEntries: ['/private'] },
    );

    render(<RouterProvider router={router} />);

    expect(screen.getByText('Login target')).toBeInTheDocument();
  });

  it('RequirePermission renders forbidden when permission is missing', () => {
    renderWithSession(
      <RequirePermission permission="users.read">
        <p>Users content</p>
      </RequirePermission>,
      { ...mockSession, permissions: [] },
    );

    expect(screen.getByRole('heading', { name: 'Forbidden' })).toBeInTheDocument();
  });
});

describe('layouts', () => {
  it('PublicLayout renders outlet', () => {
    const router = createMemoryRouter([
      {
        children: [{ element: <p>Public outlet</p>, index: true }],
        element: <PublicLayout />,
        path: '/',
      },
    ]);
    renderWithSession(<RouterProvider router={router} />);

    expect(screen.getByText('Public outlet')).toBeInTheDocument();
  });

  it('AuthLayout renders outlet', () => {
    const router = createMemoryRouter([
      {
        children: [{ element: <p>Auth outlet</p>, index: true }],
        element: <AuthLayout />,
        path: '/',
      },
    ]);
    render(<RouterProvider router={router} />);

    expect(screen.getByText('Auth outlet')).toBeInTheDocument();
  });

  it('CmsLayout renders sidebar and outlet', () => {
    const router = createMemoryRouter([
      {
        children: [{ element: <p>CMS outlet</p>, index: true }],
        element: <CmsLayout />,
        path: '/',
      },
    ]);
    renderWithSession(<RouterProvider router={router} />);

    expect(screen.getByLabelText('CMS sidebar')).toBeInTheDocument();
    expect(screen.getByText('CMS outlet')).toBeInTheDocument();
  });
});

describe('theme and state foundation', () => {
  it('Zustand sidebar state updates', () => {
    useUiStore.getState().setSidebarCollapsed(true);

    expect(useUiStore.getState().sidebarCollapsed).toBe(true);
  });

  it('ThemeProvider renders children', () => {
    render(
      <ThemeProvider>
        <p>Theme child</p>
      </ThemeProvider>,
    );

    expect(screen.getByText('Theme child')).toBeInTheDocument();
  });
});

describe('MSW foundation', () => {
  it('exports a browser worker', async () => {
    const { worker } = await import('./shared/api/mock/browser');

    expect(worker).toBeDefined();
  });
});

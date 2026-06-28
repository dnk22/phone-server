import { LoadingState } from '@repo/ui';
import { lazy, Suspense } from 'react';
import type { RouteObject } from 'react-router';

import { AuthLayout } from '../layouts/AuthLayout';

const LoginPage = lazy(() => import('../../pages/auth/login'));
const RegisterPage = lazy(() => import('../../pages/auth/register'));
const ForgotPasswordPage = lazy(() => import('../../pages/auth/forgot-password'));
const ResetPasswordPage = lazy(() => import('../../pages/auth/reset-password'));

function withSuspense(element: React.ReactNode) {
  return <Suspense fallback={<LoadingState />}>{element}</Suspense>;
}

export const authRoutes: RouteObject = {
  children: [
    { element: withSuspense(<LoginPage />), path: 'login' },
    { element: withSuspense(<RegisterPage />), path: 'register' },
    { element: withSuspense(<ForgotPasswordPage />), path: 'forgot-password' },
    { element: withSuspense(<ResetPasswordPage />), path: 'reset-password' },
  ],
  element: <AuthLayout />,
};

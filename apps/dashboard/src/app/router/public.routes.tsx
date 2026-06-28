import { LoadingState } from '@repo/ui';
import { lazy, Suspense } from 'react';
import type { RouteObject } from 'react-router';

import { PublicLayout } from '../layouts/PublicLayout';

const LandingPage = lazy(() => import('../../pages/public/landing'));
const VideoDownloaderPage = lazy(() => import('../../pages/public/video-downloader'));

function withSuspense(element: React.ReactNode) {
  return <Suspense fallback={<LoadingState />}>{element}</Suspense>;
}

export const publicRoutes: RouteObject = {
  children: [
    { element: withSuspense(<LandingPage />), index: true },
    { element: withSuspense(<VideoDownloaderPage />), path: 'video-downloader' },
  ],
  element: <PublicLayout />,
};

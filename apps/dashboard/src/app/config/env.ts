import { z } from 'zod';

type DashboardImportMetaEnv = {
  readonly DEV: boolean;
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_APP_NAME?: string;
  readonly VITE_ENABLE_MOCK_API?: string;
};

const envSchema = z.object({
  appName: z.string().min(1),
  apiBaseUrl: z.string().url(),
  enableMockApi: z.boolean(),
  isDevelopment: z.boolean(),
});

const dashboardEnv = import.meta.env as DashboardImportMetaEnv;

export const env = envSchema.parse({
  apiBaseUrl: dashboardEnv.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000',
  appName: dashboardEnv.VITE_APP_NAME ?? 'Android Linux Server',
  enableMockApi: dashboardEnv.VITE_ENABLE_MOCK_API === 'true',
  isDevelopment: dashboardEnv.DEV,
});

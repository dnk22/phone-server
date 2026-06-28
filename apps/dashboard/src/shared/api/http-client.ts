import { createHttpClient } from '@repo/api-client';

import { env } from '../../app/config/env';

export const httpClient = createHttpClient({
  baseUrl: env.apiBaseUrl,
  credentials: 'include',
});

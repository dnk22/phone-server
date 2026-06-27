import { describe, expect, it } from 'vitest';

import { createApiClient } from './index';

describe('createApiClient', () => {
  it('normalizes a trailing slash without making a network request', () => {
    expect(createApiClient({ baseUrl: 'http://127.0.0.1:8000/' }).baseUrl).toBe(
      'http://127.0.0.1:8000',
    );
  });
});

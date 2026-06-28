import { describe, expect, it } from 'vitest';

import { createHttpClient, HttpClient, queryKeys } from './index';

describe('api-client foundation', () => {
  it('creates an HTTP client without making a network request', () => {
    expect(createHttpClient({ baseUrl: 'http://127.0.0.1:8000/' })).toBeInstanceOf(HttpClient);
  });

  it('exports query keys', () => {
    expect(queryKeys.session).toEqual(['session']);
  });
});

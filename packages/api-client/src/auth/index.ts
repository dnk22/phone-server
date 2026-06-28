import type { HttpClient } from '../client/http-client';

export type SessionDto = {
  user: { id: string; name: string; email: string };
  roles: string[];
  permissions: string[];
  entitlements: string[];
};

export function createAuthApi(client: HttpClient) {
  return {
    session: (signal?: AbortSignal) =>
      client.get<SessionDto | null>('/api/v1/session', signal ? { signal } : {}),
  };
}

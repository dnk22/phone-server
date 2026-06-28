import { ApiClientError } from './errors';
import type { HttpClientOptions, RequestOptions } from './types';

export class HttpClient {
  constructor(private readonly options: HttpClientOptions) {}

  async get<T>(path: string, options: RequestOptions = {}): Promise<T> {
    return this.request<T>(path, { method: 'GET', ...options });
  }

  async post<T>(path: string, body?: unknown, options: RequestOptions = {}): Promise<T> {
    const init: RequestInit = { method: 'POST', ...options };
    if (body !== undefined) {
      init.body = JSON.stringify(body);
    }

    return this.request<T>(path, init);
  }

  private async request<T>(path: string, init: RequestInit): Promise<T> {
    const response = await fetch(new URL(path, this.options.baseUrl), {
      credentials: this.options.credentials ?? 'include',
      ...init,
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...this.options.headers,
        ...init.headers,
      },
    });

    const contentType = response.headers.get('content-type');
    const payload: unknown = contentType?.includes('application/json')
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      throw new ApiClientError(
        `Request failed with status ${response.status}`,
        response.status,
        payload,
      );
    }

    return payload as T;
  }
}

export function createHttpClient(options: HttpClientOptions) {
  return new HttpClient({
    ...options,
    baseUrl: options.baseUrl.replace(/\/$/, ''),
  });
}

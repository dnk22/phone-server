export interface ApiClientOptions {
  baseUrl: string;
}

export interface ApiClient {
  readonly baseUrl: string;
}

export function createApiClient(options: ApiClientOptions): ApiClient {
  return { baseUrl: options.baseUrl.replace(/\/$/, '') };
}

export type HttpClientOptions = {
  baseUrl: string;
  credentials?: RequestCredentials;
  headers?: HeadersInit;
};

export type RequestOptions = {
  signal?: AbortSignal;
  headers?: HeadersInit;
};

export class ApiClientError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly payload?: unknown,
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

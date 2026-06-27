export type Identifier = string;

export interface HealthStatus {
  status: 'ok' | 'degraded' | 'error';
}

export const DEFAULT_DASHBOARD_PORT = 5173;
export const DEFAULT_CONTROL_API_PORT = 8000;

export function requireEnvironmentValue(
  environment: Readonly<Record<string, string | undefined>>,
  name: string,
): string {
  const value = environment[name];
  if (!value) {
    throw new Error(`Missing environment variable: ${name}`);
  }
  return value;
}

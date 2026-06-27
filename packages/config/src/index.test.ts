import { describe, expect, it } from 'vitest';

import { requireEnvironmentValue } from './index';

describe('requireEnvironmentValue', () => {
  it('returns a configured value', () => {
    expect(requireEnvironmentValue({ APP_ENV: 'test' }, 'APP_ENV')).toBe('test');
  });

  it('rejects a missing value', () => {
    expect(() => requireEnvironmentValue({}, 'APP_ENV')).toThrow('APP_ENV');
  });
});

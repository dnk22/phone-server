import base from './packages/eslint-config/base.mjs';
import react from './packages/eslint-config/react.mjs';

export default [
  ...base,
  {
    files: ['apps/dashboard/**/*.{ts,tsx}'],
    ...react,
  },
];

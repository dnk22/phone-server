import { type SetupWorker, setupWorker } from 'msw/browser';

import { handlers } from './handlers';

const noopWorker = {
  start: () => Promise.resolve(undefined),
} as Pick<SetupWorker, 'start'>;

export const worker =
  typeof navigator !== 'undefined' && 'serviceWorker' in navigator
    ? setupWorker(...handlers)
    : noopWorker;

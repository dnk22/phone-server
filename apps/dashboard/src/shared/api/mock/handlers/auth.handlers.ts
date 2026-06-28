import { http, HttpResponse } from 'msw';

import { authFixtures } from '../fixtures';

export const authHandlers = [
  http.get('/api/v1/session', () => HttpResponse.json(authFixtures.session)),
];

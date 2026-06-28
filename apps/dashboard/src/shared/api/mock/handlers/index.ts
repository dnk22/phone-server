import { adminHandlers } from './admin.handlers';
import { authHandlers } from './auth.handlers';
import { automationHandlers } from './automation.handlers';
import { featureHandlers } from './features.handlers';
import { mediaHandlers } from './media.handlers';
import { navigationHandlers } from './navigation.handlers';

export const handlers = [
  ...authHandlers,
  ...navigationHandlers,
  ...featureHandlers,
  ...adminHandlers,
  ...automationHandlers,
  ...mediaHandlers,
];

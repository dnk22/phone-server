import { AppProviders } from './app/providers/AppProviders';
import { RouterProvider } from './app/providers/RouterProvider';

export function App() {
  return (
    <AppProviders>
      <RouterProvider />
    </AppProviders>
  );
}

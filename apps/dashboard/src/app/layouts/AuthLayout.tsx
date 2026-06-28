import { Outlet } from 'react-router';

export function AuthLayout() {
  return (
    <main className="grid min-h-screen place-items-center bg-background p-4 text-foreground">
      <section className="w-full max-w-md rounded-lg border border-border bg-card p-6">
        <Outlet />
      </section>
    </main>
  );
}

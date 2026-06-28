import { Button, Input, Label, PageHeader } from '@repo/ui';
import { useLocation } from 'react-router';

export default function LoginPage() {
  const location = useLocation();
  const redirectTo = (location.state as { redirectTo?: string } | null)?.redirectTo;

  return (
    <div className="space-y-6">
      <PageHeader
        description="Mock login foundation. Backend auth is not connected yet."
        title="Login"
      />
      {redirectTo ? (
        <p className="text-sm text-muted-foreground">After login, return to {redirectTo}.</p>
      ) : null}
      <form className="space-y-4">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" />
        <Label htmlFor="password">Password</Label>
        <Input id="password" type="password" />
        <Button type="button">Login</Button>
      </form>
    </div>
  );
}

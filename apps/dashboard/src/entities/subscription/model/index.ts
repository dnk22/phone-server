export type Subscription = {
  id: string;
  planCode: string;
  status: 'active' | 'trialing' | 'past_due' | 'cancelled';
};

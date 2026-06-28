export type AutomationTask = {
  id: string;
  status:
    | 'pending'
    | 'queued'
    | 'assigned'
    | 'accepted'
    | 'running'
    | 'succeeded'
    | 'failed'
    | 'cancelled'
    | 'timed_out';
};

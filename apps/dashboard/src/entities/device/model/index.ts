export type Device = {
  id: string;
  name: string;
  status:
    | 'unknown'
    | 'online'
    | 'offline'
    | 'unauthorized'
    | 'initializing'
    | 'ready'
    | 'busy'
    | 'error';
};

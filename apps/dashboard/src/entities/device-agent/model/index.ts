export type DeviceAgent = {
  id: string;
  name: string;
  status: 'discovered' | 'pending_pairing' | 'connected' | 'offline' | 'revoked' | 'error';
};

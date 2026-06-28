export type Feature = {
  id: string;
  code: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive';
  publicEntry: boolean;
  purchasable: boolean;
};

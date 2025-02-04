import { Inventory } from './Inventory';

export interface User {
  id: string;
  username: string;
  inventory: Inventory[];
}

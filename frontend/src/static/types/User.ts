import { Inventory } from './Inventory';

export interface User {
  _id: string;
  username: string;
  inventory: Inventory[];
}

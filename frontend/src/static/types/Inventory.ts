import { InventoryStatus } from "./Status";

export interface Inventory {
  _id: string;
  name: string;
  amount: number;
  used_by_user_ids: string[];
  image: string;
  state: InventoryStatus;
  description: string;
  updated_at: string;
  created_at: string;
}

export interface CreateInventory {
  name: string;
  amount: number;
  state: InventoryStatus;
  description: string;
}

export interface EditInventory {
  id: string;
  user_id?: string;
  name: string;
  amount: number;
  state: InventoryStatus;
  description: string;
}

import { InventoryStatus } from "./Status";

export interface Inventory {
  _id: string;
  name: string;
  amount: number;
  used_by_user_ids: string[];
  image: string;
  state: InventoryStatus;
  updated_at: string;
  created_at: string;
}

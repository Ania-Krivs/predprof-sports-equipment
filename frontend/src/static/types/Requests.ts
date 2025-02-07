import { Inventory } from "./Inventory";
import { Status } from "./Status";
import { User } from "./User";

export interface GetRequestSchema {
  inventoryId: string;
  description: string;
  amount: number;
}

export interface GetRequestResponse {
  _id: string;
  user: User;
  inventory: Inventory;
  quantity: number;
  use_purpose: string;
  status: Status;
}

export interface GetRequestStatusUpdate {
  application_id: string;
  status: Status;
}

export interface RepairRequestSchema {
  inventoryId: string;
  description: string;
}

export interface GetRequestSchema {
  inventoryId: string;
  username: string;
  description: string;
  amount: number;
}

export interface RepairRequestSchema {
  inventoryId: string;
  username: string;
  description: string;
}
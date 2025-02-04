export interface GetRequestSchema {
  inventoryId: string;
  description: string;
  amount: number;
}

export interface RepairRequestSchema {
  inventoryId: string;
  description: string;
}
export interface GetRequestSchema {
  username: string;
  equipment: string;
  amount: number;
  description: string;
}

export interface RepairRequestSchema {
  username: string;
  equipment: string;
  description: string;
}
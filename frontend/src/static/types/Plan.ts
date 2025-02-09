export interface Plan {
  _id: string;
  name: string;
  manufacturer: string;
  price: number;
}

export interface CreatePlan {
  name: string;
  manufacturer: string;
  price: number;
}
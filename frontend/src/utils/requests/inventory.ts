import { Inventory } from '../../static/types/Inventory';

export async function getInventory(): Promise<Inventory[]> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory/all_inventory/`)
  ).json();
}

export async function getInventoryById(id: string): Promise<Inventory> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory/${id}`)
  ).json();
}

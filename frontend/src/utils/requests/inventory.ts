import {
  CreateInventory,
  EditInventory,
  Inventory,
} from "../../static/types/Inventory";

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

export async function createInventory(
  inventory: CreateInventory
): Promise<string> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory/add_inventory`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(inventory),
    })
  ).json();
}

export async function editInventory(inventory: EditInventory): Promise<string> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory/update_inventory`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(inventory),
    })
  ).json();
}

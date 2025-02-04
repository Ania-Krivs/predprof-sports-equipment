import { RepairRequestSchema } from "../../static/types/Requests";

export async function repairInventoryRequest(
  token: string,
  request: RepairRequestSchema
) {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_repair/`, {
      method: "POST",
      headers: {
        token: token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        inventory_id: request.inventoryId,
        description: request.description,
        status: 0,
      }),
    })
  ).json();
}

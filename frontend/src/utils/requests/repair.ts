import {
  RepairRequestResponse,
  RepairRequestSchema,
} from "../../static/types/Requests";

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

export async function getAllRepairRequests(
  token: string
): Promise<RepairRequestResponse[]> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_repair/all/${token}`)
  ).json();
}

export async function deleteRepairRequest(token: string, id: string) {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_repair/${token}`, {
      method: "DELETE",
      headers: {
        token: token,
        "application-id": id,
        "Content-Type": "application/json",
      },
    })
  ).json();
}

import {
  GetRequestResponse,
  GetRequestSchema,
} from "../../static/types/Requests";

export async function invokeGetInventoryRequest(
  token: string,
  request: GetRequestSchema
) {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_application/`, {
      method: "POST",
      headers: {
        token: token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        inventory_id: request.inventoryId,
        amount: request.amount,
        use_purpose: request.description,
      }),
    })
  ).json();
}

export async function getInventoryRequests(
  token: string
): Promise<GetRequestResponse[]> {
  return await (
    await fetch(
      `${import.meta.env.VITE_API_URL}/inventory_application/user/${token}`,
      {
        headers: {
          token: token,
        },
      }
    )
  ).json();
}

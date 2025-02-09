import { Plan, CreatePlan } from "../../static/types/Plan";

export async function getPlan(token: string): Promise<Plan[]> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_plan`, {
      headers: {
        "admin-token": token,
      },
    })
  ).json();
}

export async function addToPlan(token: string, plan: CreatePlan) {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/inventory_plan`, {
      method: "POST",
      headers: {
        "admin-token": token,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(plan),
    })
  ).json();
}

export async function deleteFromPlan(token: string, id: string) {
  return await (
    await fetch(
      `${import.meta.env.VITE_API_URL}/inventory_plan/${id}?admin_token=${token}`,
      {
        method: "DELETE",
      }
    )
  ).json();
}

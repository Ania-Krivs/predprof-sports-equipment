import { User } from "../../static/types/User";

export async function loginUser(
  login: string,
  password: string,
  admin: boolean
): Promise<string> {
  const res = await (
    await fetch(
      `${import.meta.env.VITE_API_URL}/${admin ? "admin" : "user"}/log_in`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: login,
          password: password,
        }),
      }
    )
  ).json();
  return admin ? res.admin_token : res.user_token;
}

export async function registerUser(
  login: string,
  password: string
): Promise<string> {
  return (
    await (
      await fetch(`${import.meta.env.VITE_API_URL}/user/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: login,
          password: password,
        }),
      })
    ).json()
  ).user_token;
}

export async function getUser(token: string): Promise<User> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/user`, {
      headers: {
        token: token,
      },
    })
  ).json();
}

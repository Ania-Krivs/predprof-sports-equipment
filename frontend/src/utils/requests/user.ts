import { User } from "../../static/types/User";

interface LoginResponse {
  user_token: string;
}

export async function loginUser(
  login: string,
  password: string
): Promise<LoginResponse> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/user/log_in`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: login,
        password: password,
      }),
    })
  ).json();
}

export async function registerUser(
  login: string,
  password: string
): Promise<LoginResponse> {
  return await (
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
  ).json();
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

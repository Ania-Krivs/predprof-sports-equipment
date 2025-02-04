interface LoginResponse {
  user_token: string;
}

export async function loginUser(
  login: string,
  password: string
): Promise<LoginResponse> {
  return await (
    await fetch(`${import.meta.env.VITE_API_URL}/user/login`, {
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

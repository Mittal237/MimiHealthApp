import { Platform } from "react-native";

function getBaseUrl() {
  if (Platform.OS === "android") {
    return "http://10.0.2.2:8000";
  }

  const deviceIp = "10.0.0.171"; // 
  return `http://${deviceIp}:8000`;
}

const BASE = getBaseUrl();

async function handle(res: Response) {
  const text = await res.text();
  if (!res.ok) throw new Error(text || `HTTP ${res.status}`);
  try {
    return JSON.parse(text);
  } catch {
    return text as any;
  }
}

export const api = {
  signup: async (data: any) => {
    const res = await fetch(`${BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return handle(res);
  },

  setupProfile: async (data: any) => {
    const res = await fetch(`${BASE}/auth/profile/setup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    return handle(res);
  },

  generateWeek: async (userId: string) => {
    const res = await fetch(`${BASE}/plan/generate-week?userId=${userId}`, {
      method: "POST",
    });
    return handle(res);
  },

  getCurrentPlan: async (userId: string) => {
    const res = await fetch(`${BASE}/plan/current?userId=${userId}`);
    return handle(res);
  },
};

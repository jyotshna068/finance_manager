const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function getToken() {
  return localStorage.getItem("access_token");
}

async function request(endpoint, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Something went wrong");
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/pdf")) {
    return response.blob();
  }
  return response.json();
}

export const api = {
  register: (data) =>
    request("/auth/register", { method: "POST", body: JSON.stringify(data) }),

  login: (data) =>
    request("/auth/login", { method: "POST", body: JSON.stringify(data) }),

  uploadStatement: (file, accountId) => {
    const formData = new FormData();
    formData.append("file", file);
    if (accountId) formData.append("account_id", accountId);

    const token = getToken();
    return fetch(`${BASE_URL}/upload/statement`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    }).then(async (res) => {
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Upload failed" }));
        throw new Error(err.detail);
      }
      return res.json();
    });
  },

  getAnalysis: () => request("/dashboard/analysis"),

  generateReport: () => request("/reports/generate", { method: "POST" }),

  getReportHistory: () => request("/reports/history"),
};

export function saveAuth(token, userId) {
  localStorage.setItem("access_token", token);
  localStorage.setItem("user_id", userId);
}

export function clearAuth() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_id");
}

export function isAuthenticated() {
  return !!getToken();
}

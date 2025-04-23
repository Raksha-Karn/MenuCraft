const API_URL = "/api/";

export const apiService = {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem("accessToken");
    if (token) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      };
    }

    let response = await fetch(`${API_URL}${endpoint}`, options);

    if (response.status === 401) {
      const refreshed = await this.refreshToken();

      if (refreshed) {
        const newToken = localStorage.getItem("accessToken");
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${newToken}`,
        };
        response = await fetch(`${API_URL}${endpoint}`, options);
      }
    }

    return response;
  },

  async refreshToken() {
    const refreshToken = localStorage.getItem("refreshToken");

    if (!refreshToken) {
      return false;
    }

    try {
      const response = await fetch(`${API_URL}auth/token/refresh/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        return false;
      }

      const data = await response.json();
      localStorage.setItem("accessToken", data.access);
      return true;
    } catch (error) {
      console.error("Token refresh failed:", error);
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      return false;
    }
  },

  async get(endpoint) {
    return this.request(endpoint);
  },

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  },

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  },

  async delete(endpoint) {
    return this.request(endpoint, {
      method: "DELETE",
    });
  },
};

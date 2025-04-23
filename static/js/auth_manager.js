document.addEventListener("DOMContentLoaded", function () {
  function isAuthenticated() {
    return localStorage.getItem("accessToken") !== null;
  }

  function updateAuthUI() {
    const desktopAuthLinks = document.getElementById("auth-links-desktop");
    const mobileAuthLinks = document.getElementById("auth-links-mobile");

    if (isAuthenticated()) {
      desktopAuthLinks.innerHTML = `
                <a href="/dashboard" class="hover:text-primary transition">Dashboard</a>
                <a href="#" id="logout-btn-desktop" class="hover:text-primary transition">Logout</a>
            `;

      mobileAuthLinks.innerHTML = `
                <a href="/dashboard" class="hover:text-primary transition">Dashboard</a>
                <a href="#" id="logout-btn-mobile" class="hover:text-primary transition">Logout</a>
            `;

      document
        .getElementById("logout-btn-desktop")
        ?.addEventListener("click", handleLogout);
      document
        .getElementById("logout-btn-mobile")
        ?.addEventListener("click", handleLogout);
    } else {
      desktopAuthLinks.innerHTML = `
                <a href="/login" class="hover:text-primary transition">Login</a>
                <a href="/register" class="hover:text-primary transition">Register</a>
            `;

      mobileAuthLinks.innerHTML = `
                <a href="/login" class="hover:text-primary transition">Login</a>
                <a href="/register" class="hover:text-primary transition">Register</a>
            `;
    }
  }

  function handleLogout(e) {
    e.preventDefault();
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");

    window.location.href = "/";
  }

  updateAuthUI();
});

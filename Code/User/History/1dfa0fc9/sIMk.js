// Simple frontend auth script
(function () {
  // Get key from URL params
  function getKeyParam() {
    const params = new URLSearchParams(window.location.search);
    return params.get("key");
  }

  async function validateKey(key) {
    try {
      const res = await fetch(
        "https://nazarcwel.vercel.app/api/validate?key=" + encodeURIComponent(key)
      );
      const data = await res.json();
      return data.valid;
    } catch (e) {
      return false;
    }
  }

  async function checkAuth() {
    const key = getKeyParam();
    if (!key) {
      window.location.href = "login.html";
      return;
    }
    const valid = await validateKey(key);
    if (!valid) {
      window.location.href = "login.html";
    }
  }

  // Only run on protected pages
  if (!window.location.pathname.includes("/login/")) {
    checkAuth();
  }
})();

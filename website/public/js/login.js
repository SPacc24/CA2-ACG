document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const alertBox = document.getElementById("alertBox");
  const loginBtn = document.getElementById("loginBtn");

  alertBox.classList.add("d-none");
  alertBox.textContent = "";

  if (!username || !password) {
    showError("Please enter both username and password.");
    return;
  }

  loginBtn.disabled = true;
  loginBtn.textContent = "Logging in...";

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Login failed");
    }

    // Success
    window.location.href = "upload.html";

  } catch (err) {
    showError(err.message);
  } finally {
    loginBtn.disabled = false;
    loginBtn.textContent = "Login";
  }

  function showError(message) {
    alertBox.textContent = message;
    alertBox.classList.remove("d-none");
  }
});

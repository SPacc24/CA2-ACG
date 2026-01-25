document.getElementById("loginForm").addEventListener("submit", async e => {
  e.preventDefault();

  const res = await fetch("http://SERVER_IP:5000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  });

  const data = await res.json();
  document.getElementById("msg").innerText = data.message;

  if (data.success) {
    window.location.href = "./upload.html";
  }
});

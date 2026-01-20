async function upload() {
  const files = document.getElementById("files").files;
  const form = new FormData();

  for (let f of files) {
    form.append("files", f);
  }

  const res = await fetch("http://SERVER_IP:5001/upload", {
    method: "POST",
    body: form
  });

  document.getElementById("msg").innerText =
    (await res.json()).message;
}

const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const statusBox = document.getElementById("statusBox");
const logoutBtn = document.getElementById("logoutBtn");

uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    showStatus("Please select a file or folder.", "danger");
    return;
  }

  const formData = new FormData();

  for (const file of fileInput.files) {
    formData.append("files", file, file.webkitRelativePath || file.name);
  }

  try {
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";

    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message);
    }

    showStatus("Upload successful. Encryption applied.", "success");

  } catch (err) {
    showStatus(err.message, "danger");
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload Securely";
  }
});

logoutBtn.addEventListener("click", () => {
  fetch("/logout", { method: "POST" })
    .then(() => window.location.href = "login.html");
});

function showStatus(msg, type) {
  statusBox.textContent = msg;
  statusBox.className = `alert alert-${type} mt-3`;
  statusBox.classList.remove("d-none");
}

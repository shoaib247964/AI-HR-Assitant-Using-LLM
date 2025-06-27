async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage("You", message, "user");
  input.value = "";

  // Show typing indicator
  showTyping(true);

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    addMessage("AI", data.response, "ai");
  } catch (e) {
    addMessage("AI", "Sorry, I couldn't process your request. Please try again later.", "ai");
  } finally {
    // Hide typing indicator
    showTyping(false);
  }
}

function addMessage(sender, text, type) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = `bubble ${type}`;
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function showTyping(show) {
  const typing = document.getElementById("typing-indicator");
  typing.style.display = show ? "flex" : "none";
}

// File upload logic
const fileInput = document.getElementById("fileInput");
const fileUploadBtn = document.querySelector(".file-upload-btn");
if (fileInput && fileUploadBtn) {
  fileInput.addEventListener("change", async function() {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      addMessage("You", `Uploading <em>${file.name}</em>...`, "user");
      const formData = new FormData();
      formData.append("file", file);
      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData
        });
        const data = await response.json();
        if (data.success) {
          addMessage("AI", `File <em>${file.name}</em> uploaded successfully!`, "ai");
        } else {
          addMessage("AI", `File upload failed: ${data.message}`, "ai");
        }
      } catch (e) {
        addMessage("AI", "File upload failed. Please try again.", "ai");
      }
    }
  });
} 
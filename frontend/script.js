// script.js
const API_BASE = ""; // agar same origin pe hai to empty

let currentSessionId = null;
let isTyping = false;

// DOM Elements
const chatArea = document.getElementById("chatArea");
const welcomeScreen = document.getElementById("welcomeScreen");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const sessionsList = document.getElementById("sessionsList");
const newChatBtn = document.getElementById("newChatBtn");
const typingIndicator = document.getElementById("typingIndicator");
const crisisModal = document.getElementById("crisisModal");
const modalClose = document.getElementById("modalClose");
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");
const sidebarClose = document.getElementById("sidebarClose");

// Auto resize textarea
userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
});

// Send Message
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message || isTyping) return;

  if (!currentSessionId) {
    await createNewSession();
  }

  // Add user message to UI
  addMessageToUI("user", message);
  userInput.value = "";
  userInput.style.height = "auto";

  showTypingIndicator();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: currentSessionId,
        message: message,
      }),
    });

    const data = await res.json();

    hideTypingIndicator();

    if (data.reply) {
      addMessageToUI("aura", data.reply, data.type);

      // Show crisis modal if needed
      if (data.type === "crisis") {
        setTimeout(() => {
          crisisModal.style.display = "flex";
        }, 800);
      }
    }
  } catch (err) {
    hideTypingIndicator();
    addMessageToUI(
      "aura",
      "Sorry, I'm having trouble connecting right now. Please try again.",
    );
  }
}

// Add message to chat UI
function addMessageToUI(role, content, type = "normal") {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role} ${type}`;

  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  messageDiv.innerHTML = `
        <div class="msg-avatar">
            ${role === "aura" ? '<i class="fa-solid fa-brain"></i>' : '<i class="fa-solid fa-user"></i>'}
        </div>
        <div>
            <div class="msg-bubble">${content}</div>
            <div class="msg-time">${time}</div>
        </div>
    `;

  chatArea.appendChild(messageDiv);
  chatArea.scrollTop = chatArea.scrollHeight;
}

// Typing Indicator
function showTypingIndicator() {
  isTyping = true;
  typingIndicator.style.display = "flex";
  chatArea.scrollTop = chatArea.scrollHeight;
}

function hideTypingIndicator() {
  isTyping = false;
  typingIndicator.style.display = "none";
}

// Create New Session
async function createNewSession() {
  try {
    const res = await fetch("/api/new-session", { method: "POST" });
    const data = await res.json();
    currentSessionId = data.session_id;
    chatArea.innerHTML = ""; // Clear previous chat
    welcomeScreen.style.display = "none";
    return currentSessionId;
  } catch (e) {
    console.error("Failed to create new session");
  }
}

// Load Sessions List
async function loadSessions() {
  try {
    const res = await fetch("/api/sessions");
    const sessions = await res.json();

    sessionsList.innerHTML = "";

    if (sessions.length === 0) {
      sessionsList.innerHTML = `<div class="sessions-loading">No previous sessions</div>`;
      return;
    }

    sessions.forEach((session) => {
      const div = document.createElement("div");
      div.className = `session-item ${session.id === currentSessionId ? "active" : ""}`;
      div.textContent = session.preview || "New Conversation";
      div.onclick = () => loadSessionHistory(session.id);
      sessionsList.appendChild(div);
    });
  } catch (e) {
    sessionsList.innerHTML = `<div class="sessions-loading">Failed to load sessions</div>`;
  }
}

// Load Specific Session History
async function loadSessionHistory(sessionId) {
  currentSessionId = sessionId;
  chatArea.innerHTML = "";
  welcomeScreen.style.display = "none";

  try {
    const res = await fetch(`/api/history/${sessionId}`);
    const data = await res.json();

    data.history.forEach((msg) => {
      addMessageToUI(msg.role === "user" ? "user" : "aura", msg.content);
    });
  } catch (e) {
    console.error("Failed to load history");
  }

  loadSessions(); // Refresh active state
}

// Event Listeners
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

newChatBtn.addEventListener("click", async () => {
  await createNewSession();
  loadSessions();
});

modalClose.addEventListener("click", () => {
  crisisModal.style.display = "none";
});

// Mobile Menu
menuBtn.addEventListener("click", () => {
  sidebar.classList.add("open");
});

sidebarClose.addEventListener("click", () => {
  sidebar.classList.remove("open");
});

// Suggestion Chips
document.querySelectorAll(".suggestion-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    userInput.value = chip.dataset.text;
    sendMessage();
  });
});

// Mood Buttons
document.querySelectorAll(".mood-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document
      .querySelectorAll(".mood-btn")
      .forEach((b) => b.classList.remove("selected"));
    btn.classList.add("selected");

    const moodText = `I'm feeling ${btn.dataset.mood}`;
    userInput.value = moodText;
    sendMessage();
  });
});

// Initialize App
async function init() {
  await loadSessions();

  // Auto start a new session if none selected
  if (!currentSessionId) {
    await createNewSession();
  }
}

window.onload = init;

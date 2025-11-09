const API_URL = "http://127.0.0.1:8000/chat"; // Local FastAPI endpoint
const DEBUG = true; // Set to true to show debug information

// Debug logging function
function debugLog(message, data = null) {
    if (!DEBUG) return;
    
    const debugDiv = document.getElementById('debugInfo');
    if (debugDiv) {
        debugDiv.style.display = 'block';
        debugDiv.innerHTML = `<strong>Debug:</strong> ${message}<br>` + 
            (data ? `<pre>${JSON.stringify(data, null, 2)}</pre>` : '');
        console.log(message, data);
    }
}

// Get or create a session ID from localStorage
function getSessionId() {
    let sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
        sessionId = "user_" + Math.floor(Math.random() * 1000000);
        localStorage.setItem('chatSessionId', sessionId);
    }
    debugLog('Using session ID:', sessionId);
    return sessionId;
}

// Check server connection on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/');
        if (response.ok) {
            debugLog('Server connection successful');
        } else {
            debugLog('Server returned error:', response.status);
        }
    } catch (err) {
        debugLog('Server connection failed:', err.message);
    }
});

function toggleChat() {
    const chat = document.getElementById("chatWidget");
    if (chat) {
        chat.style.display = chat.style.display === "flex" ? "none" : "flex";
    }
}

function appendMessage(role, text) {
    const box = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = role.toLowerCase() === "bot" ? "bot-message" : "user-message";
    msg.innerHTML = `<strong>${role}:</strong> ${text}`;
    msg.style.margin = "8px 0";
    msg.style.padding = "8px 12px";
    msg.style.borderRadius = "8px";
    msg.style.backgroundColor = role.toLowerCase() === "bot" ? "#f0f4f8" : "#e3f2fd";
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    // Disable input while processing
    input.disabled = true;
    const sendButton = input.nextElementSibling;
    sendButton.disabled = true;
    
    // Add loading indicator to button
    const originalButtonText = sendButton.innerHTML;
    sendButton.innerHTML = '<div class="loading"></div>Sending...';

    appendMessage("You", text);
    input.value = "";

    try {
        console.log('Sending request to:', API_URL);
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({ 
                session_id: getSessionId(), 
                query: text 
            }),
        });

        console.log('Response status:', res.status);
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const data = await res.json();
        console.log('Response data:', data);
        
        if (data.error) {
            appendMessage("Bot", "Error: " + data.response);
        } else {
            appendMessage("Bot", data.response);
        }
    } catch (err) {
        console.error('Chat error:', err);
        appendMessage("Bot", "I'm sorry, but I'm having trouble: " + err.message);
    } finally {
        // Re-enable input and restore button
        input.disabled = false;
        sendButton.disabled = false;
        sendButton.innerHTML = originalButtonText;
        input.focus();
    }
}
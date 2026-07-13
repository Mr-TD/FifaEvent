/**
 * StadiumIQ — Chatbot JavaScript
 * AI-powered conversational assistant
 */

const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const typingIndicator = document.getElementById('typing-indicator');

// Send message on Enter
if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && chatInput.value.trim()) {
            sendMessage();
        }
    });
}

function sendSuggestion(text) {
    chatInput.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    const language = document.getElementById('language-select').value;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';

    // Show typing indicator
    typingIndicator.classList.add('active');
    scrollToBottom();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, language })
        });

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.classList.remove('active');

        // Add AI response
        addMessage(data.response, 'ai');
    } catch (error) {
        typingIndicator.classList.remove('active');
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;

    const avatar = sender === 'ai' ? '🤖' : '👤';
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Convert markdown-style bold
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div>
            <div class="message-bubble">${formattedText}</div>
            <div class="message-time">${now}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

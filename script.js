document.addEventListener('DOMContentLoaded', function () {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const languageDropdown = document.getElementById('language-dropdown');
    const themeToggle = document.getElementById('theme-toggle');

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender);
        messageDiv.textContent = `${sender === 'user' ? 'You' : 'JusticePal AI'}: ${message}`;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        const language = languageDropdown.value;

        if (message === '') return;

        // Show user message in chat
        appendMessage('user', message);

        // Clear input
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message, language })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            appendMessage('bot', data.botReply);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('bot', 'Sorry, there was an error processing your request.');
        }
    }

    // Send button click event
    sendBtn.addEventListener('click', sendMessage);

    // Enter key event
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Theme toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
    });
});

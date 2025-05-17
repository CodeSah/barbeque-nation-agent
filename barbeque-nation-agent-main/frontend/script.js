const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

function appendMessage(message, sender) {
    const div = document.createElement('div');
    div.className = sender === 'user' ? 'user-msg' : 'bot-msg';
    div.textContent = message;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendQuery() {
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage(question, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ property: "Delhi", question: question }) // Change property if needed
        });
        const data = await response.json();
        appendMessage(data.response || "Sorry, no response.", 'bot');
    } catch (error) {
        appendMessage("Error connecting to server.", 'bot');
    }
}

sendBtn.addEventListener('click', sendQuery);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendQuery();
});

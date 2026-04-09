function addMessage(text, className) {
    const chat = document.getElementById("chat");

    const div = document.createElement("div");
    div.className = "message " + className;
    div.innerText = text;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
    const chat = document.getElementById("chat");

    const div = document.createElement("div");
    div.className = "message bot";
    div.id = "typing";

    div.innerHTML = `
        <div class="typing">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

function addCard(rec) {
    const chat = document.getElementById("chat");

    const div = document.createElement("div");
    div.className = "message bot";

    div.innerHTML = `
        <strong>${rec.technique}</strong><br>
        Score: ${rec.score}<br>
        ${rec.explanation}<br><br>

        <button onclick="sendFeedback('${rec.technique}', true)">LIKE</button>
        <button onclick="sendFeedback('${rec.technique}', false)">DISLIKE</button>
    `;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// QUICK FILL (for suggestion buttons)
function quickFill(text) {
    document.getElementById("input").value = text;
}

async function send() {
    const input = document.getElementById("input");
    const text = input.value;

    if (!text) return;

    // HIDE EMPTY STATE
    const emptyState = document.getElementById("emptyState");
    if (emptyState) emptyState.style.display = "none";

    addMessage(text, "user");
    input.value = "";

    showTyping();

    const res = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ texts: [text] })
    });

    const data = await res.json();

    removeTyping();

    data.recommendations.forEach((r, i) => {
        setTimeout(() => addCard(r), i * 300);
    });
}

async function sendFeedback(technique, liked) {
    await fetch("http://127.0.0.1:8000/feedback", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "user1",
            technique: technique,
            liked: liked
        })
    });
}
from flask import Flask, request, jsonify, render_template_string
from log_to_sheet import log_conversation
import json
import re

app = Flask(__name__)

# Load knowledge base
with open('knowledge_base.json', 'r') as f:
    KNOWLEDGE_BASE = json.load(f)

# Token limiter
def truncate_to_800_tokens(text):
    words = text.split()
    return ' '.join(words[:600])  # Approx. 800 tokens

# Extract booking details using regex
def extract_booking_details(text):
    match = re.search(
        r'(?P<name>[a-zA-Z\s]+),\s*(?P<phone>\d{10}),\s*(?P<guests>\d+),\s*(?P<date>[\w\s\d]+),\s*(?P<time>[\w\d\s\.]+)',
        text
    )
    if match:
        return match.groupdict()
    return None

# Chatbot UI HTML
CHATBOT_HTML = """
<!DOCTYPE html>
<html>
<head><title>Barbeque Nation Chatbot</title></head>
<body>
<h2>Welcome to Barbeque Nation Chatbot</h2>
<div>
    <label for="property">Select City: </label>
    <select id="property">
        <option value="Delhi">Delhi</option>
        <option value="Bangalore">Bangalore</option>
    </select>
</div>
<div id="chat" style="border:1px solid #ccc; padding:10px; height:300px; overflow:auto; margin-top:10px;"></div>
<input type="text" id="userInput" placeholder="Ask something..." style="width:70%;" />
<button onclick="sendQuery()">Send</button>

<script>
async function sendQuery() {
    const question = document.getElementById('userInput').value.trim();
    const property = document.getElementById('property').value;
    if (!question) return;

    const response = await fetch('/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question, property })
    });
    const data = await response.json();
    const chatDiv = document.getElementById('chat');
    chatDiv.innerHTML += `<p><b>You (${property}):</b> ${question}</p>`;
    chatDiv.innerHTML += `<p><b>Bot:</b> ${data.response}</p>`;
    chatDiv.scrollTop = chatDiv.scrollHeight;
    document.getElementById('userInput').value = '';
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(CHATBOT_HTML)


@app.route('/query', methods=['POST'])
def query():
    data = request.json
    property_name = data.get("property", "").strip()
    user_question = data.get("question", "").strip().lower()

    if not property_name or property_name not in KNOWLEDGE_BASE:
        return jsonify({"response": "Please select a valid property."})

    responses = KNOWLEDGE_BASE[property_name].get("responses", [])
    matched = None

    # Try to match intent
    for resp in responses:
        if resp["intent"].lower() in user_question:
            matched = resp
            break

    booking_details = extract_booking_details(data["question"])

    # If intent matched
    if matched:
        response_text = truncate_to_800_tokens(matched["response"])

        # If it's a booking intent, log details if present
        if matched["intent"].lower() == "booking" and booking_details:
            try:
                log_conversation({
                    "Modality": "Web Chat",
                    "Call Time": "NA",
                    "Phone Number": booking_details["phone"],
                    "Call Outcome": "Booking Taken",
                    "Room Name": property_name,
                    "Booking Date": booking_details["date"],
                    "Booking Time": booking_details["time"],
                    "Number of Guests": booking_details["guests"],
                    "Call Summary": f"Booking for {booking_details['name']}",
                })
            except Exception as e:
                print(f"[Logging Error] {e}")

        return jsonify({"response": response_text})

    # If no intent matched, but booking details are detected
    if booking_details:
        try:
            log_conversation({
                "Modality": "Web Chat",
                "Call Time": "NA",
                "Phone Number": booking_details["phone"],
                "Call Outcome": "Booking Taken",
                "Room Name": property_name,
                "Booking Date": booking_details["date"],
                "Booking Time": booking_details["time"],
                "Number of Guests": booking_details["guests"],
                "Call Summary": f"Booking for {booking_details['name']}",
            })
            return jsonify(
                {"response": "Thanks! Your booking has been received. We’ll see you soon at our Delhi outlet."})
        except Exception as e:
            return jsonify({"response": f"Booking received, but failed to log: {e}"})

    return jsonify({"response": "Sorry, I couldn't find information related to your query."})


@app.route('/log', methods=['POST'])
def log():
    data = request.json
    try:
        log_conversation(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

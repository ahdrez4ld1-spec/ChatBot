import requests
import json
import time
from chatbot import SimpleChatbot
from flask import Flask, request, jsonify, render_template_string
from threading import Thread
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Template HTML sederhana untuk testing
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Chatbot Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chat-container { max-width: 600px; margin: 0 auto; }
        .message { padding: 10px; margin: 5px 0; border-radius: 10px; }
        .user-message { background-color: #0084ff; color: white; text-align: right; }
        .bot-message { background-color: #f1f0f0; color: black; }
        .input-area { margin-top: 20px; }
        input[type="text"] { width: 80%; padding: 10px; }
        button { padding: 10px 20px; background-color: #0084ff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>🤖 Instagram Onyetbot Test</h1>
        <div id="chat-messages">
            <div class="message bot-message">Halo! Aku adalah onyetbot Instagram. Kirim pesan untuk mencoba!</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Ketik pesan Anda..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Kirim</button>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            
            if (message) {
                // Tampilkan pesan user
                addMessage(message, 'user-message');
                input.value = '';
                
                // Kirim ke server dan dapatkan respons
                fetch('/test-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'bot-message');
                })
                .catch(error => {
                    addMessage('Maaf, ada error: ' + error, 'bot-message');
                });
            }
        }
        
        function addMessage(text, className) {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = text;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    </script>
</body>
</html>
'''

class TestInstagramBot:
    def __init__(self):
        self.chatbot = SimpleChatbot()
        
    def process_message(self, user_message):
        """Memproses pesan menggunakan chatbot"""
        return self.chatbot.get_response(user_message)

# Flask Web App
app = Flask(__name__)
test_bot = TestInstagramBot()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/test-chat', methods=['POST'])
def test_chat():
    """Endpoint untuk testing chat"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Dapatkan respons dari chatbot
        response = test_bot.process_message(user_message)
        
        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({
            'status': 'error',
            'response': 'Maaf, ada kesalahan dalam memproses pesan Anda.'
        }), 500

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'bot_name': 'Test Instagram Chatbot',
        'mode': 'testing'
    })

if __name__ == '__main__':
    logger.info("Starting Test Instagram Chatbot...")
    print("🚀 Test Instagram Chatbot is running!")
    print("🌐 Open http://localhost:5000 in your browser")
    print("💡 This is a test version - no Instagram integration required")
    print("❌ Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
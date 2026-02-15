import requests
import json
import time
from chatbot import SimpleChatbot
from flask import Flask, request, jsonify
from threading import Thread
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramBot:
    def __init__(self, access_token, instagram_account_id):
        self.access_token = access_token
        self.account_id = instagram_account_id
        self.chatbot = SimpleChatbot()
        self.base_url = "https://graph.instagram.com"
        self.graph_url = "https://graph.facebook.com/v18.0"
        
    def get_conversations(self):
        """Mendapatkan daftar percakapan"""
        try:
            url = f"{self.graph_url}/{self.account_id}/conversations"
            params = {
                'access_token': self.access_token,
                'fields': 'participants,unread_count,updated_time'
            }
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting conversations: {e}")
            return {}
    
    def get_messages(self, conversation_id):
        """Mendapatkan pesan dari percakapan tertentu"""
        try:
            url = f"{self.graph_url}/{conversation_id}/messages"
            params = {
                'access_token': self.access_token,
                'fields': 'message,from,created_time'
            }
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            return {}
    
    def send_message(self, recipient_id, message_text):
        """Mengirim pesan ke pengguna"""
        try:
            url = f"{self.graph_url}/me/messages"
            data = {
                'recipient': {'id': recipient_id},
                'message': {'text': message_text},
                'access_token': self.access_token
            }
            response = requests.post(url, json=data)
            logger.info(f"Message sent to {recipient_id}: {message_text}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {}
    
    def process_new_messages(self):
        """Memproses pesan baru"""
        try:
            conversations = self.get_conversations()
            
            for conversation in conversations.get('data', []):
                if conversation.get('unread_count', 0) > 0:
                    messages = self.get_messages(conversation['id'])
                    
                    # Proses pesan terbaru
                    for message in messages.get('data', []):
                        if message.get('from', {}).get('id') != self.account_id:
                            user_message = message.get('message', '')
                            user_id = message['from']['id']
                            
                            # Dapatkan respons dari chatbot
                            bot_response = self.chatbot.get_response(user_message)
                            
                            # Kirim respons
                            self.send_message(user_id, bot_response)
                            
                            logger.info(f"Processed message from {user_id}: {user_message}")
                            
        except Exception as e:
            logger.error(f"Error processing messages: {e}")

# Flask Web App untuk Webhook
app = Flask(__name__)
instagram_bot = None

@app.route('/')
def index():
    return '''
    <h1>Instagram Chatbot</h1>
    <p>Bot is running and listening for Instagram messages</p>
    <p>Status: <span id="status">Active</span></p>
    '''

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifikasi webhook untuk Instagram"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Ganti 'your_verify_token' dengan token verifikasi Anda
    if mode == 'subscribe' and token == 'instagram_chatbot_verify_token':
        logger.info("Webhook verified successfully")
        return challenge
    else:
        return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Menerima notifikasi webhook dari Instagram"""
    try:
        data = request.json
        logger.info(f"Webhook received: {json.dumps(data, indent=2)}")
        
        # Proses notifikasi
        if data.get('object') == 'instagram':
            # Jalankan pemrosesan pesan di thread terpisah
            thread = Thread(target=process_webhook_data, args=(data,))
            thread.start()
        
        return 'EVENT_RECEIVED', 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return 'Error', 500

def process_webhook_data(data):
    """Memproses data webhook di thread terpisah"""
    try:
        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                if messaging.get('message'):
                    sender_id = messaging['sender']['id']
                    message_text = messaging['message']['text']
                    
                    # Dapatkan respons dari chatbot
                    response = instagram_bot.chatbot.get_response(message_text)
                    
                    # Kirim respons
                    instagram_bot.send_message(sender_id, response)
                    logger.info(f"Auto-replied to {sender_id}: {response}")
                    
    except Exception as e:
        logger.error(f"Error in webhook processing: {e}")

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'bot_name': 'Instagram Chatbot',
        'last_check': time.strftime('%Y-%m-%d %H:%M:%S')
    })

def start_message_polling():
    """Mulai polling pesan secara berkala"""
    while True:
        try:
            if instagram_bot:
                instagram_bot.process_new_messages()
            time.sleep(30)  # Cek setiap 30 detik
        except Exception as e:
            logger.error(f"Error in message polling: {e}")
            time.sleep(60)  # Tunggu 1 menit jika ada error

if __name__ == '__main__':
    # Konfigurasi - GANTI DENGAN NILAI YANG SESUAI
    ACCESS_TOKEN = "YOUR_INSTAGRAM_ACCESS_TOKEN"
    INSTAGRAM_ACCOUNT_ID = "YOUR_INSTAGRAM_ACCOUNT_ID"
    
    # Inisialisasi bot
    instagram_bot = InstagramBot(ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID)
    
    # Mulai thread polling
    polling_thread = Thread(target=start_message_polling)
    polling_thread.daemon = True
    polling_thread.start()
    
    # Jalankan Flask app
    logger.info("Starting Instagram Chatbot...")
    app.run(host='0.0.0.0', port=5000, debug=False)
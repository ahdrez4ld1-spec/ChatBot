import random
import re
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Template HTML untuk chatbot cerdas
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart Critical Thinking Chatbot</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .chat-container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .chat-messages { 
            height: 400px; 
            overflow-y: auto; 
            padding: 20px;
            background: #f8f9fa;
        }
        .message { 
            padding: 12px 16px; 
            margin: 10px 0; 
            border-radius: 18px; 
            max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message { 
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white; 
            margin-left: auto;
            text-align: right;
        }
        .bot-message { 
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }
        .input-area { 
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
        }
        input[type="text"] { 
            flex: 1;
            padding: 15px; 
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #4facfe;
        }
        button { 
            padding: 15px 25px; 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white; 
            border: none; 
            border-radius: 25px;
            margin-left: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .thinking {
            color: #666;
            font-style: italic;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>🤖 Onyet Bot - Berpikir Kritis</h1>
            <p>Chatbot dengan kemampuan analisis dan pemikiran mendalam</p>
        </div>
        <div id="chat-messages" class="chat-messages">
            <div class="message bot-message">Halo! Saya adalah chatbot dengan kemampuan berpikir kritis. Saya bisa menganalisis pertanyaan secara mendalam dan memberikan respons yang lebih bermakna. Apa yang ingin Anda diskusikan hari ini?</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Sampaikan pertanyaan atau pemikiran Anda..." onkeypress="handleKeyPress(event)">
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
                
                // Tampilkan indikator berpikir
                const thinking = addMessage('Sedang menganalisis...', 'thinking');
                
                // Kirim ke server dan dapatkan respons
                fetch('/smart-chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Hapus indikator berpikir
                    thinking.remove();
                    // Tampilkan respons
                    addMessage(data.response, 'bot-message');
                })
                .catch(error => {
                    thinking.remove();
                    addMessage('Maaf, ada error dalam proses berpikir: ' + error, 'bot-message');
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
            return messageDiv;
        }
    </script>
</body>
</html>
'''

class SmartChatbot:
    def __init__(self):
        # Knowledge base untuk topik umum dengan analisis kritis
        self.knowledge_base = {
            'teknologi': [
                "Teknologi AI memang revolusioner, tapi kita perlu mempertimbangkan etika dan dampak sosialnya. Keseimbangan antara inovasi dan tanggung jawab sangat penting.",
                "Digitalisasi mengubah cara kita bekerja dan berinteraksi. Tantangannya adalah memastikan manfaatnya dirasakan semua lapisan masyarakat, bukan hanya segelintir orang.",
                "Perkembangan teknologi seharusnya melayani kemanusiaan, bukan sebaliknya. Kita perlu kritis terhadap narrative 'teknologi untuk segalanya'."
            ],
            'pendidikan': [
                "Sistem pendidikan idealnya menumbuhkan kreativitas dan kemampuan berpikir kritis, bukan hanya menghafal informasi. Paradigma perlu diubah.",
                "Pendidikan karakter dan literasi digital sama pentingnya dengan literasi akademik. Generasi masa depan perlu keterampilan abad 21.",
                "Akses pendidikan yang merata adalah hak asasi. Ketimpangan pendidikan menciptakan ketimpangan sosial yang lebih luas."
            ],
            'lingkungan': [
                "Krisis lingkungan memerlukan aksi segera dari individu, korporasi, dan pemerintah. Tanggung jawab kolektif sangat krusial.",
                "Solusi lingkungan tidak hanya tentang teknologi, tapi juga perubahan perilaku dan sistemik. Pendekatan holistik diperlukan.",
                "Keadilan iklim menjadi isu penting - negara maju yang lebih banyak berkontribusi terhadap polusi seharusnya membantu negara berkembang."
            ],
            'sosial': [
                "Media sosial mengubah dinamika sosial secara fundamental. Kita perlu literasi digital untuk memahami dampaknya pada psikologi dan masyarakat.",
                "Perbedaan pandangan seharusnya menjadi kekuatan, bukan sumber konflik. Dialog antar kelompok berbeda sangat penting.",
                "Kesetaraan gender, ras, dan kelas masih menjadi tantangan besar. Perubahan memerlukan kesadaran dan aksi kolektif."
            ],
            'ekonomi': [
                "Ketimpangan ekonomi menciptakan masalah sosial yang lebih besar. Kebijakan progresif diperlukan untuk menciptakan distribusi yang lebih adil.",
                "Ekonomi berkelanjutan harus mempertimbangkan kesejahteraan manusia dan lingkungan, bukan hanya pertumbuhan GDP.",
                "Otomatisasi akan mengubah pasar kerja secara fundamental. Persiapan dan adaptasi menjadi kunci untuk masa depan."
            ],
            'politik': [
                "Demokrasi memerlukan partisipasi aktif warga. Literasi politik dan kritis terhadap informasi sangat penting.",
                "Transparansi dan akuntabilitas adalah pilar utama pemerintahan yang baik. Sistem checks and balances harus dijaga.",
                "Kebijakan publik seharusnya berdasarkan evidence dan kepentingan rakyat, bukan kepentingan kelompok tertentu."
            ]
        }
        
        # Pattern analisis kritis
        self.critical_patterns = {
            'analisis': r'\b(apa penyebab|kenapa|mengapa|alasan|faktor|analisis|sebab|akibat)\b',
            'evaluasi': r'\b(apakah baik|bagaimana efektif|pro kontra|kelebihan|kekurangan|manfaat|dampak)\b',
            'solusi': r'\b(bagaimana cara|solusi|cara mengatasi|langkah|pendekatan|strategi)\b',
            'perbandingan': r'\b(lebih baik|perbedaan|bandingkan|vs|versus|dibandingkan)\b',
            'prediksi': r'\b(akan terjadi|masa depan|ke depan|tren|perkembangan|kecenderungan)\b',
            'argumen': r'\b(setuju|tidak setuju|pendapat|opini|keyakinan|sikap)\b'
        }
        
        # Respons kritis yang lebih mendalam
        self.critical_responses = {
            'analisis': [
                "Mari kita telusuri akar permasalahan ini dengan pendekatan sistemik...",
                "Dari perspektif kritis, beberapa faktor interdependen perlu dipertimbangkan...",
                "Analisis holistik menunjukkan bahwa ini adalah isu multifaset...",
                "Jika kita eksplor lebih dalam, beberapa dimensi penting muncul..."
            ],
            'evaluasi': [
                "Evaluasi ini memerlukan pendekatan multidimensi dan objektif...",
                "Mari kita lihat dari berbagai perspektif untuk evaluasi yang seimbang...",
                "Pertimbangan pro dan kontra menunjukkan kompleksitas isu ini...",
                "Evaluasi kritis mengungkap beberapa trade-off yang perlu dipertimbangkan..."
            ],
            'solusi': [
                "Solusi efektif memerlukan pendekatan integratif dan berkelanjutan...",
                "Mari eksplor beberapa strategi inovatif yang mungkin diterapkan...",
                "Solusi terbaik seringkali kombinasi dari pendekatan teknis dan manusiawi...",
                "Pendekatan sistemik diperlukan untuk mengatasi akar permasalahan..."
            ],
            'perbandingan': [
                "Perbandingan yang menarik! Mari lihat trade-off dan konteks masing-masing...",
                "Setiap pendekatan memiliki trade-offs unik yang perlu dipertimbangkan...",
                "Dari analisis komparatif, beberapa insight strategis muncul...",
                "Perbandingan ini mengungkap kompleksitas dalam pengambilan keputusan..."
            ],
            'prediksi': [
                "Berdasarkan tren dan analisis data, beberapa skenario menarik mungkin terjadi...",
                "Prediksi memerlukan pertimbangan multiple variables dan uncertainties...",
                "Melihat ke masa depan, beberapa faktor kunci akan mempengaruhi trajectory...",
                "Tren saat ini menunjukkan beberapa kemungkinan yang perlu kita antisipasi..."
            ],
            'argumen': [
                "Perspektif menarik! Mari eksplor logika dan asumsi di balik pandangan ini...",
                "Argumen ini memiliki beberapa titik kuat, tapi juga asumsi yang perlu dipertanyakan...",
                "Mari kita telusuri lebih dalam validitas dan soundness dari reasoning ini...",
                "Pandangan ini membuka diskusi penting tentang nilai-nilai dan prinsip yang mendasari..."
            ]
        }
        
        # Pola deteksi topik
        self.topic_patterns = {
            'teknologi': r'\b(ai|artificial intelligence|machine learning|teknologi|digital|komputer|internet|smartphone|robot|innovasi)\b',
            'pendidikan': r'\b(sekolah|universitas|belajar|pendidikan|guru|siswa|kurikulum|pembelajaran|literasi)\b',
            'lingkungan': r'\b(lingkungan|alam|polusi|iklim|sustainable|green|ekologi|climate change|carbon|emisi)\b',
            'sosial': r'\b(masyarakat|sosial|budaya|tradisi|norma|interaksi|komunitas|sosial media|media)\b',
            'ekonomi': r'\b(ekonomi|uang|bisnis|pasar|inflasi|krisis|pertumbuhan|investasi|ketimpangan)\b',
            'politik': r'\b(politik|pemerintah|hukum|kebijakan|demokrasi|pemilihan|keadilan|governance)\b'
        }

    def analyze_input(self, user_input):
        """Analisis input pengguna secara komprehensif"""
        user_input_lower = user_input.lower()
        
        # Deteksi jenis analisis kritis
        analysis_type = None
        for crit_type, pattern in self.critical_patterns.items():
            if re.search(pattern, user_input_lower):
                analysis_type = crit_type
                break
        
        # Deteksi topik
        detected_topic = None
        for topic, pattern in self.topic_patterns.items():
            if re.search(pattern, user_input_lower):
                detected_topic = topic
                break
        
        # Deteksi kompleksitas (panjang dan struktur)
        word_count = len(user_input.split())
        has_question_mark = '?' in user_input
        has_complex_question_words = any(word in user_input_lower for word in 
                                       ['bagaimana', 'mengapa', 'kenapa', 'sebab', 'akibat'])
        
        complexity = 'high' if (word_count > 10 or has_complex_question_words) else 'medium' if word_count > 5 else 'low'
        
        return {
            'analysis_type': analysis_type,
            'topic': detected_topic,
            'complexity': complexity,
            'has_question': has_question_mark,
            'word_count': word_count
        }

    def generate_response(self, user_input, analysis):
        """Generate respons cerdas berdasarkan analisis"""
        # Jika ada jenis analisis kritis terdeteksi
        if analysis['analysis_type']:
            intro = random.choice(self.critical_responses[analysis['analysis_type']])
            
            # Jika ada topik spesifik
            if analysis['topic'] and analysis['topic'] in self.knowledge_base:
                topic_insight = random.choice(self.knowledge_base[analysis['topic']])
                return f"{intro} {topic_insight}"
            else:
                return f"{intro} Ini adalah isu kompleks yang memerlukan pertimbangan mendalam dari berbagai perspektif."
        
        # Jika ada topik tapi tidak ada analisis khusus
        elif analysis['topic'] and analysis['topic'] in self.knowledge_base:
            topic_response = random.choice(self.knowledge_base[analysis['topic']])
            return f"Dari perspektif kritis, {topic_response.lower()}"
        
        # Untuk pertanyaan umum
        elif analysis['has_question'] or any(word in user_input.lower() for word in 
              ['apa', 'bagaimana', 'kenapa', 'mengapa', 'siapa', 'kapan', 'dimana']):
            return "Pertanyaan yang menarik! Mari kita eksplor bersama dari berbagai perspektif dan sudut pandang yang mungkin."
        
        # Respons default untuk statement
        else:
            return "Perspektif menarik! Bisakah Anda jelaskan lebih detail atau bagikan pemikiran di balik pandangan ini? Saya tertarik untuk memahami konteksnya lebih dalam."

    def get_response(self, user_input):
        """Main response function"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Silakan sampaikan pertanyaan atau pemikiran Anda. Saya siap untuk diskusi yang mendalam dan bermakna."
        
        # Handle greetings
        if re.search(r'\b(hello|hi|hey|halo|hai|selamat)\b', user_input.lower()):
            return "Halo! Saya senang bisa berdiskusi dengan Anda. Saya siap untuk eksplorasi ide-ide menarik secara kritis dan mendalam. Apa yang ingin Anda diskusikan?"
        
        # Analisis dan generate respons
        analysis = self.analyze_input(user_input)
        return self.generate_response(user_input, analysis)

# Flask Web App
app = Flask(__name__)
smart_bot = SmartChatbot()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/smart-chat', methods=['POST'])
def smart_chat():
    """Endpoint untuk chatbot cerdas"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Dapatkan respons cerdas
        response = smart_bot.get_response(user_message)
        
        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({
            'status': 'error',
            'response': 'Maaf, ada kesalahan dalam proses berpikir saya. Bisakah Anda ulangi pertanyaan Anda?'
        }), 500

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'bot_name': 'Smart Critical Thinking Chatbot',
        'version': '2.0'
    })

if __name__ == '__main__':
    logger.info("Starting Smart Critical Thinking Chatbot...")
    print("🚀 Smart Critical Thinking Chatbot is running!")
    print("🌐 Open http://localhost:5000 in your browser")
    print("💡 This version features advanced critical thinking capabilities")
    print("❌ Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
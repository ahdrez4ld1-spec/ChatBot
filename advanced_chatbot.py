import random
import re
import json
from datetime import datetime

class AdvancedChatbot:
    def __init__(self):
        # Knowledge base untuk topik umum
        self.knowledge_base = {
            'teknologi': [
                "Teknologi terus berkembang pesat. Dari AI hingga quantum computing, inovasi baru muncul setiap hari.",
                "Saya melihat teknologi sebagai alat yang bisa membantu atau menghambat, tergantung bagaimana kita menggunakannya.",
                "Perkembangan teknologi memang mengagumkan, tapi kita juga perlu mempertimbangkan dampak sosialnya."
            ],
            'pendidikan': [
                "Pendidikan adalah fondasi kemajuan bangsa. Investasi dalam pendidikan berdampak jangka panjang.",
                "Sistem pendidikan idealnya menyesuaikan dengan kebutuhan individu, bukan sebaliknya.",
                "Literasi digital menjadi semakin penting di era informasi seperti sekarang."
            ],
            'lingkungan': [
                "Isu lingkungan memerlukan aksi kolektif. Perubahan kecil dari individu bisa berdampak besar.",
                "Keseimbangan antara pembangunan ekonomi dan pelestarian lingkungan sangat krusial.",
                "Generasi muda memiliki peran penting dalam menyelesaikan tantangan lingkungan global."
            ],
            'sosial': [
                "Masalah sosial kompleks dan saling terkait. Solusi memerlukan pendekatan multidimensi.",
                "Empati dan dialog terbuka adalah kunci untuk memahami perspektif berbeda.",
                "Perubahan sosial dimulai dari kesadaran individu dan komitmen kolektif."
            ]
        }
        
        # Pola pertanyaan kritis
        self.critical_thinking_patterns = {
            'analisis': r'\b(apa penyebab|kenapa|mengapa|alasan|faktor|analisis)\b',
            'evaluasi': r'\b(apakah baik|bagaimana efektif|pro kontra|kelebihan|kekurangan)\b',
            'solusi': r'\b(bagaimana cara|solusi|cara mengatasi|langkah|pendekatan)\b',
            'perbandingan': r'\b(lebih baik|perbedaan|bandingkan|vs|versus)\b',
            'prediksi': r'\b(akan terjadi|masa depan|ke depan|tren|perkembangan)\b'
        }
        
        # Respons kritis untuk berbagai jenis pertanyaan
        self.critical_responses = {
            'analisis': [
                "Mari kita analisis dari beberapa sudut pandang...",
                "Pertanyaan bagus! Jika kita telusuri lebih dalam...",
                "Dari perspektif kritis, saya melihat beberapa faktor penting...",
                "Analisis yang menarik. Beberapa poin yang perlu dipertimbangkan..."
            ],
            'evaluasi': [
                "Ini evaluasi yang kompleks. Mari kita lihat pro dan kontranya...",
                "Pertanyaan evaluatif memerlukan pendekatan objektif...",
                "Dari berbagai perspektif, saya bisa memberikan analisis...",
                "Evaluasi ini memiliki banyak dimensi yang perlu dipertimbangkan..."
            ],
            'solusi': [
                "Solusi yang efektif memerlukan pendekatan sistematis...",
                "Mari kita eksplor beberapa pendekatan yang mungkin...",
                "Solusi terbaik seringkali kombinasi dari beberapa strategi...",
                "Pendekatan inovatif mungkin diperlukan untuk tantangan ini..."
            ],
            'perbandingan': [
                "Perbandingan yang menarik! Mari kita lihat sisi-sisinya...",
                "Setiap pendekatan memiliki kelebihan dan kekurangan...",
                "Dari analisis komparatif, beberapa poin penting muncul...",
                "Perbandingan ini membuka perspektif baru yang menarik..."
            ],
            'prediksi': [
                "Berdasarkan tren saat ini, beberapa skenario mungkin terjadi...",
                "Prediksi memerlukan analisis data dan pemahaman konteks...",
                "Melihat ke masa depan, beberapa faktor akan mempengaruhi...",
                "Tren saat ini menunjukkan beberapa kemungkinan menarik..."
            ]
        }
        
        # Respons umum yang lebih cerdas
        self.intelligent_responses = {
            'greeting': [
                "Halo! Saya senang bisa berdiskusi dengan Anda hari ini. Ada topik menarik yang ingin dibahas?",
                "Selamat datang! Saya siap untuk percakapan yang mendalam dan bermakna.",
                "Hai! Mari kita eksplor ide-ide menarik bersama. Apa yang sedang Anda pikirkan?"
            ],
            'question': [
                "Pertanyaan yang menarik! Mari kita eksplor bersama...",
                "Saya senang Anda bertanya itu. Dari perspektif kritis...",
                "Topik yang kompleks. Beberapa poin penting yang perlu dipertimbangkan...",
                "Pertanyaan bagus! Mari kita analisis dari berbagai sudut pandang..."
            ],
            'default': [
                "Perspektif menarik! Bisakah Anda jelaskan lebih detail?",
                "Saya mencoba memahami sudut pandang Anda. Apakah ada aspek spesifik yang ingin didiskusikan?",
                "Topik ini memiliki banyak dimensi. Aspek mana yang paling menarik bagi Anda?",
                "Saya tertarik dengan pemikiran Anda. Bisakah kita eksplor lebih dalam?"
            ]
        }
        
        # Pola deteksi topik
        self.topic_patterns = {
            'teknologi': r'\b(ai|artificial intelligence|machine learning|teknologi|digital|komputer|internet|smartphone|robot)\b',
            'pendidikan': r'\b(sekolah|universitas|belajar|pendidikan|guru|siswa|kurikulum|pembelajaran)\b',
            'lingkungan': r'\b(lingkungan|alam|polusi|iklim|sustainable|green|ekologi|alam sekitar)\b',
            'sosial': r'\b(masyarakat|sosial|budaya|tradisi|norma|interaksi|komunitas|sosial media)\b',
            'ekonomi': r'\b(ekonomi|uang|bisnis|pasar|inflasi|krisis|pertumbuhan|investasi)\b',
            'politik': r'\b(politik|pemerintah|hukum|kebijakan|demokrasi|pemilihan|keadilan)\b'
        }

    def analyze_question_type(self, user_input):
        """Menganalisis jenis pertanyaan untuk respons yang tepat"""
        user_input_lower = user_input.lower()
        
        # Deteksi jenis pertanyaan kritis
        for question_type, pattern in self.critical_thinking_patterns.items():
            if re.search(pattern, user_input_lower):
                return question_type
        
        # Deteksi topik
        for topic, pattern in self.topic_patterns.items():
            if re.search(pattern, user_input_lower):
                return f"topic_{topic}"
        
        return "general"

    def get_topic_response(self, topic):
        """Memberikan respons berdasarkan topik yang terdeteksi"""
        clean_topic = topic.replace("topic_", "")
        if clean_topic in self.knowledge_base:
            return random.choice(self.knowledge_base[clean_topic])
        return None

    def get_critical_response(self, question_type):
        """Memberikan respons kritis berdasarkan jenis pertanyaan"""
        if question_type in self.critical_responses:
            return random.choice(self.critical_responses[question_type])
        return random.choice(self.critical_responses['analisis'])

    def generate_intelligent_response(self, user_input):
        """Generate respons cerdas berdasarkan input pengguna"""
        question_type = self.analyze_question_type(user_input)
        
        # Jika pertanyaan kritis terdeteksi
        if question_type in self.critical_thinking_patterns:
            critical_intro = self.get_critical_response(question_type)
            topic_response = None
            
            # Cek apakah ada topik spesifik
            for topic in self.topic_patterns:
                if re.search(self.topic_patterns[topic], user_input.lower()):
                    topic_response = self.get_topic_response(f"topic_{topic}")
                    break
            
            if topic_response:
                return f"{critical_intro} {topic_response}"
            else:
                return f"{critical_intro} Ini adalah topik yang kompleks yang memerlukan analisis mendalam."
        
        # Jika topik terdeteksi
        elif question_type.startswith("topic_"):
            topic_response = self.get_topic_response(question_type)
            if topic_response:
                return f"{random.choice(self.intelligent_responses['question'])} {topic_response}"
        
        # Respons umum untuk pertanyaan
        elif '?' in user_input or any(word in user_input.lower() for word in 
              ['apa', 'bagaimana', 'kenapa', 'mengapa', 'siapa', 'kapan', 'dimana']):
            return random.choice(self.intelligent_responses['question'])
        
        # Respons default
        else:
            return random.choice(self.intelligent_responses['default'])

    def get_response(self, user_input):
        """Generate response based on user input with critical thinking"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Silakan sampaikan pertanyaan atau pemikiran Anda. Saya siap untuk berdiskusi secara mendalam."
        
        # Handle greetings
        greeting_patterns = r'\b(hello|hi|hey|halo|hai|selamat pagi|selamat siang|selamat sore|selamat malam)\b'
        if re.search(greeting_patterns, user_input.lower()):
            return random.choice(self.intelligent_responses['greeting'])
        
        # Generate intelligent response
        return self.generate_intelligent_response(user_input)

    def chat(self):
        """Main chat loop with enhanced critical thinking"""
        print("🤖 Onyet Bot - Versi Berpikir Kritis")
        print("=" * 50)
        print("Halo! Saya adalah chatbot dengan kemampuan berpikir kritis.")
        print("Saya bisa menganalisis pertanyaan secara mendalam dan memberikan respons yang lebih bermakna.")
        print("Ketik 'quit' untuk keluar.")
        print()
        
        while True:
            try:
                user_input = input("Anda: ").strip()
                
                # Exit condition
                if user_input.lower() in ['quit', 'exit', 'bye', 'keluar']:
                    print("ChatBot: Terima kasih atas diskusi yang menarik! Sampai jumpa!")
                    break
                
                # Handle empty input
                if not user_input:
                    print("ChatBot: Silakan sampaikan pemikiran Anda. Saya siap untuk berdiskusi!")
                    continue
                
                # Get and print intelligent response
                response = self.get_response(user_input)
                print(f"ChatBot: {response}")
                print()
                
            except KeyboardInterrupt:
                print("\n\nChatBot: Diskusi yang menarik! Sampai jumpa lain waktu!")
                break
            except Exception as e:
                print(f"ChatBot: Maaf, ada kesalahan: {e}")

def main():
    """Main function to run the advanced chatbot"""
    chatbot = AdvancedChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
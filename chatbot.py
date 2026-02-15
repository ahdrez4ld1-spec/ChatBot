import random
import re
from datetime import datetime

class SimpleChatbot:
    def __init__(self):
        # Dictionary of responses for different patterns (Indonesian)
        self.responses = {
            'greeting': [
                "Halo! Bagaimana aku bisa membantu Anda hari ini?",
                "Hai! Ada yang bisa aku bantu?",
                "Selamat datang! Senang bertemu dengan Anda!",
                "Halo! Apa kabar Anda hari ini?"
            ],
            'goodbye': [
                "Selamat tinggal! Semoga harimu menyenangkan!",
                "Sampai jumpa lagi!",
                "Hati-hati ya!",
                "Dadah! Datang lagi kapan-kapan!"
            ],
            'how_are_you': [
                "Aku baik-baik saja, terima kasih sudah bertanya!",
                "Aku Kangen! Terima kasih sudah menanyakan.",
                "Aku baik, bagaimana dengan Anda?",
                "Semuanya baik di sini! Apakah saya bisa membantu Anda?"
            ],
            'name': [
                "Aku adalah onyet bot sederhana yang dibuat untuk membantu Anda!",
                "Anda bisa memanggil saya onyet!",
                "Aku adalah asisten onyet yang ramah!",
                "Aku hanya onyet, tapi Anda bisa menganggap saya sebagai teman digital Anda!"
            ],
            'help': [
                "Aku bisa mengobrol dengan Anda! Coba tanyakan bagaimana kabar aku, siapa nama aku, atau cukup ucapkan halo!",
                "Aku di sini untuk mengobrol dengan Anda. Tanyakan apa saja!",
                "Aku bisa merespons salam, pertanyaan tentang diri aku, dan percakapan dasar!",
                "Cukup berbicara dengan aku secara alami dan aku akan melakukan yang terbaik untuk merespons!"
            ],
            'question': [
                "Itu adalah pertanyaan yang menarik! Berikut pendapat aku...",
                "Aku senang Anda bertanya itu. Menurut aku...",
                "Pertanyaan bagus! Aku pikir...",
                "Aku memahami pertanyaan Anda. Jawabannya mungkin...",
                "Terima kasih atas pertanyaan Anda! Menurut aku...",
                "Wah, pertanyaan yang hebat! Mari kita bahas...",
                "Aku suka tantangan ini. Jawabannya kira-kira...",
                "Pertanyaan cerdas! Aku rasa...",
                "Menarik sekali pertanyaan Anda. Pendapat aku...",
                "Aku senang bisa membantu menjawab pertanyaan ini. Jawabannya..."
            ],
            'default': [
                "Menarik! Ceritakan lebih banyak.",
                "Aku mengerti. Apa lagi yang ingin Anda bahas?",
                "Hmm, aku tidak yakin aku mengerti. Bisakah Anda mengulanginya?",
                "Itu bagus! Hal apa yang paling Anda sukai tentang itu?",
                "Aku masih belajar, tapi aku di sini untuk mengobrol dengan Anda!",
                "Aku senang Anda berbagi informasi ini. Ada hal lain yang ingin didiskusikan?",
                "Terima kasih atas informasi ini. Apakah Anda punya pertanyaan lebih lanjut?",
                "Aku mencoba memahami. Bisakah Anda memberikan lebih banyak detail?",
                "Itulah perspektif yang menarik. Bagaimana pendapat Anda tentang topik lain?",
                "Aku terbuka untuk berdiskusi lebih lanjut tentang hal ini."
            ]
        }
        
        # Patterns to match user input (Indonesian and English)
        self.patterns = {
            'greeting': r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening|halo|hai|selamat pagi|selamat siang|selamat sore|selamat malam)\b',
            'goodbye': r'\b(bye|goodbye|see you|farewell|later|dadah|selamat tinggal|sampai jumpa)\b',
            'how_are_you': r'\b(how are you|how do you do|how\'s it going|how are things|apa kabar|kabar|gimana kabar)\b',
            'name': r'\b(what is your name|who are you|what should I call you|siapa namamu|siapa kamu|nama kamu apa)\b',
            'help': r'\b(help|what can you do|assist|support|bantu|tolong|bisa bantu)\b',
            'question': r'\b(apa|bagaimana|berapa|siapa|kapan|dimana|kenapa|why|what|how|when|where|who|which|whose|whom|pertanyaan|tentang)\b'
        }
    
    def get_response(self, user_input):
        """Generate a response based on user input with critical thinking"""
        original_input = user_input
        user_input = user_input.lower().strip()
        
        # Enhanced critical thinking patterns
        critical_thinking_patterns = {
            'analisis': r'\b(apa penyebab|kenapa|mengapa|alasan|faktor|analisis|sebab|akibat)\b',
            'evaluasi': r'\b(apakah baik|bagaimana efektif|pro kontra|kelebihan|kekurangan|manfaat|dampak)\b',
            'solusi': r'\b(bagaimana cara|solusi|cara mengatasi|langkah|pendekatan|strategi)\b',
            'perbandingan': r'\b(lebih baik|perbedaan|bandingkan|vs|versus|dibandingkan)\b',
            'prediksi': r'\b(akan terjadi|masa depan|ke depan|tren|perkembangan|kecenderungan)\b',
            'argumen': r'\b(setuju|tidak setuju|pendapat|opini|keyakinan|sikap)\b'
        }
        
        # Check for critical thinking patterns
        for crit_type, pattern in critical_thinking_patterns.items():
            if re.search(pattern, user_input):
                if crit_type == 'analisis':
                    return "Mari kita telusuri akar permasalahan ini dengan pendekatan sistemik... Ini adalah isu kompleks yang memerlukan pertimbangan mendalam dari berbagai perspektif."
                elif crit_type == 'evaluasi':
                    return "Evaluasi ini memerlukan pendekatan multidimensi dan objektif. Mari kita lihat dari berbagai perspektif untuk evaluasi yang seimbang..."
                elif crit_type == 'solusi':
                    return "Solusi efektif memerlukan pendekatan integratif dan berkelanjutan. Mari eksplor beberapa strategi inovatif yang mungkin diterapkan..."
                elif crit_type == 'perbandingan':
                    return "Perbandingan yang menarik! Mari lihat trade-off dan konteks masing-masing. Setiap pendekatan memiliki trade-offs unik yang perlu dipertimbangkan..."
                elif crit_type == 'prediksi':
                    return "Berdasarkan tren dan analisis data, beberapa skenario menarik mungkin terjadi. Melihat ke masa depan, beberapa faktor kunci akan mempengaruhi trajectory..."
                elif crit_type == 'argumen':
                    return "Perspektif menarik! Mari eksplor logika dan asumsi di balik pandangan ini. Pandangan ini membuka diskusi penting tentang nilai-nilai dan prinsip yang mendasari..."
        
        # Check for matching patterns
        for category, pattern in self.patterns.items():
            if re.search(pattern, user_input):
                return random.choice(self.responses[category])
        
        # Check if input contains a question mark, treat as question
        if '?' in user_input:
            return random.choice(self.responses['question'])
        
        # Check for common question words that might not match patterns
        question_indicators = ['apakah', 'bisakah', 'bolehkah', 'mengapa', 'kenapa', 'bagaimana', 'apa', 'siapa', 'dimana', 'kapan', 'berapa']
        if any(indicator in user_input for indicator in question_indicators):
            return random.choice(self.responses['question'])
        
        # If input is quite long, it might be a complex question or statement
        if len(user_input.split()) > 5:
            # Check if it seems like a question by looking for question-like structures
            if any(word in user_input for word in [' tentang ', ' mengenai ', ' perihal ', ' tentang ', 'about', 'regarding', 'concerning']):
                return random.choice(self.responses['question'])
            else:
                return random.choice(self.responses['default'])
        
        # If no pattern matches, return a default response
        return random.choice(self.responses['default'])
    
    def chat(self):
        """Main chat loop"""
        print("🤖 Onyet Bot Sederhana")
        print("=" * 30)
        print("Halo! Aku adalah chatbot sederhana. Ketik 'quit' untuk keluar.")
        print()
        
        while True:
            try:
                user_input = input("Anda: ").strip()
                
                # Exit condition
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("ChatBot: Selamat tinggal! Terima kasih sudah mengobrol!")
                    break
                
                # Handle empty input
                if not user_input:
                    print("ChatBot: Silakan katakan sesuatu!")
                    continue
                
                # Get and print response
                response = self.get_response(user_input)
                print(f"ChatBot: {response}")
                print()
                
            except KeyboardInterrupt:
                print("\n\nChatBot: Selamat tinggal! Terima kasih sudah mengobrol!")
                break
            except Exception as e:
                print(f"ChatBot: Maaf, ada yang salah: {e}")

def main():
    """Main function to run the chatbot"""
    chatbot = SimpleChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main()
    
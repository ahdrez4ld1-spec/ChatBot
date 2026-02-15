import random
import re
import json
import math
from datetime import datetime
from collections import defaultdict

class UniversalAIBot:
    def __init__(self):
        # Expanded knowledge base with multiple domains
        self.knowledge_base = {
            'science': {
                'physics': [
                    "Fisika adalah ilmu yang mempelajari materi, energi, gerak, dan gaya fundamental alam semesta.",
                    "Prinsip-prinsip fisika membentuk dasar teknologi modern dari smartphone hingga pesawat luar angkasa.",
                    "Fisika kuantum mengungkap perilaku partikel subatomik yang tampaknya kontra-intuitif tapi sangat penting."
                ],
                'chemistry': [
                    "Kimia adalah ilmu yang mempelajari susunan, struktur, dan sifat zat serta perubahan kimia.",
                    "Reaksi kimia terjadi ketika ikatan antar atom terbentuk atau putus, menciptakan senyawa baru.",
                    "Kimia organik mempelajari senyawa karbon yang merupakan dasar kehidupan."
                ],
                'biology': [
                    "Biologi mempelajari makhluk hidup dan proses-proses kehidupan dari mikroskopis hingga ekosistem.",
                    "Teori evolusi Darwin menjelaskan bagaimana spesies berubah seiring waktu melalui seleksi alam.",
                    "DNA adalah kode genetik yang membawa informasi untuk sintesis protein dan pewarisan sifat."
                ],
                'astronomy': [
                    "Astronomi adalah studi tentang objek dan fenomena di luar atmosfer bumi.",
                    "Galaksi Bima Sakti kita adalah rumah bagi miliaran bintang, termasuk matahari kita.",
                    "Teori Big Bang menjelaskan asal usul alam semesta sekitar 13.8 miliar tahun lalu."
                ]
            },
            'technology': {
                'ai_ml': [
                    "AI dan Machine Learning merevolusi cara kita memecahkan masalah kompleks dengan data.",
                    "Deep Learning meniru struktur otak manusia dalam jaringan saraf buatan untuk pengenalan pola.",
                    "Ethical AI menjadi penting karena keputusan AI semakin mempengaruhi kehidupan sehari-hari."
                ],
                'programming': [
                    "Pemrograman adalah seni dan ilmu menciptakan instruksi untuk komputer menyelesaikan tugas.",
                    "Paradigma pemrograman berbeda (OO, FP, procedural) menawarkan pendekatan berbeda untuk desain solusi.",
                    "Software engineering menekankan praktik terbaik untuk membuat perangkat lunak yang dapat dipelihara."
                ],
                'hardware': [
                    "Hardware komputer adalah komponen fisik yang menjalankan instruksi perangkat lunak.",
                    "Moore's Law menjelaskan bagaimana jumlah transistor di chip berkembang secara eksponensial.",
                    "Quantum computing menjanjikan kekuatan komputasi yang jauh melampaui komputer klasik."
                ]
            },
            'society': {
                'politics': [
                    "Politik adalah proses pengambilan keputusan kolektif yang mempengaruhi seluruh masyarakat.",
                    "Demokrasi idealnya memberikan suara kepada rakyat dalam menentukan pemimpin dan kebijakan.",
                    "Good governance memerlukan transparansi, akuntabilitas, dan partisipasi warga."
                ],
                'economics': [
                    "Ekonomi mempelajari bagaimana masyarakat mengalokasikan sumber daya yang terbatas.",
                    "Supply and demand adalah mekanisme fundamental dalam menentukan harga di pasar.",
                    "Ketidaksetaraan ekonomi menjadi tantangan global yang memerlukan kebijakan redistributif."
                ],
                'education': [
                    "Pendidikan adalah investasi jangka panjang dalam kapital manusia dan kesejahteraan sosial.",
                    "Literasi digital menjadi penting sejalan dengan transformasi digital di semua bidang.",
                    "Pendidikan kritis menghasilkan warga yang mampu berpikir analitis dan etis."
                ]
            },
            'culture': {
                'philosophy': [
                    "Filsafat mengeksplorasi pertanyaan mendasar tentang eksistensi, pengetahuan, dan nilai-nilai.",
                    "Epistemologi mempelajari sifat dan batas pengetahuan manusia.",
                    "Etika normatif membantu kita memahami apa yang benar dan salah dalam tindakan moral."
                ],
                'arts': [
                    "Seni mencerminkan dan membentuk budaya serta memfasilitasi ekspresi emosi dan ide.",
                    "Kritik seni mengevaluasi karya dari segi estetika, konteks historis, dan dampak sosial.",
                    "Seni dan teknologi semakin terintegrasi dalam bentuk media digital dan instalasi interaktif."
                ]
            }
        }
        
        # Expanded question patterns for different types
        self.question_patterns = {
            'definition': [
                r'\bapa itu|apa arti|definisi|pengertian|arti kata\b',
                r'\bwhat is|meaning of|define|definition of\b'
            ],
            'comparison': [
                r'\bbandingkan|perbedaan|lebih baik|vs|versus\b',
                r'\bcompare|difference|better|versus\b'
            ],
            'causal': [
                r'\bkenapa|mengapa|penyebab|sebab|alasan\b',
                r'\bwhy|cause|reason|because\b'
            ],
            'process': [
                r'\bbagaimana cara|bagaimana|proses|mekanisme\b',
                r'\bhow|process|mechanism|way to\b'
            ],
            'prediction': [
                r'\bakan terjadi|masa depan|tren|perkembangan\b',
                r'\bwill happen|future|trend|development\b'
            ],
            'evaluation': [
                r'\bapakah baik|bagus|buruk|efektif|manjur\b',
                r'\bis it good|effective|worth it|valuable\b'
            ],
            'solution': [
                r'\bsolusi|cara mengatasi|penyelesaian|alternatif\b',
                r'\bsolution|how to solve|ways to|alternatives\b'
            ],
            'historical': [
                r'\bsaat kapan|kapan terjadi|sejarah|riwayat\b',
                r'\bwhen|history|origin|past event\b'
            ]
        }
        
        # Response templates for different question types
        self.response_templates = {
            'definition': [
                "Konsep {concept} merujuk pada...",
                "{concept} adalah istilah yang menggambarkan...",
                "Dalam konteks ini, {concept} berarti..."
            ],
            'comparison': [
                "Perbedaan utama antara {item1} dan {item2} adalah...",
                "Dari segi karakteristik, {item1} dan {item2} berbeda dalam beberapa aspek penting...",
                "Jika kita bandingkan {item1} dengan {item2}, beberapa perbedaan muncul..."
            ],
            'causal': [
                "Beberapa faktor utama yang menyebabkan {phenomenon} meliputi...",
                "Penyebab utama {phenomenon} adalah kombinasi dari...",
                "Alasan di balik {phenomenon} bisa dijelaskan dari berbagai perspektif..."
            ],
            'process': [
                "Proses {process} melibatkan beberapa tahapan penting...",
                "Secara umum, {process} berlangsung melalui langkah-langkah berikut...",
                "Mekanisme {process} dapat dijelaskan sebagai berikut..."
            ],
            'prediction': [
                "Berdasarkan tren saat ini, beberapa kemungkinan untuk {future_event} adalah...",
                "Jika tren saat ini berlanjut, {future_event} kemungkinan akan...",
                "Prospek untuk {future_event} tergantung pada beberapa variabel penting..."
            ],
            'evaluation': [
                "Dari berbagai perspektif, {subject} memiliki kelebihan dan kekurangan...",
                "Efektivitas {subject} tergantung pada konteks dan kriteria evaluasi...",
                "Penilaian terhadap {subject} harus mempertimbangkan berbagai faktor..."
            ],
            'solution': [
                "Beberapa pendekatan yang mungkin untuk mengatasi {problem} meliputi...",
                "Solusi efektif untuk {problem} memerlukan pendekatan yang sistematis...",
                "Ada beberapa strategi yang bisa dipertimbangkan untuk {problem}..."
            ],
            'historical': [
                "{event} terjadi pada {time_period} dalam konteks sejarah yang lebih luas...",
                "Peristiwa {event} merupakan bagian dari perkembangan sejarah {context}...",
                "Tanggal {time_period} menandai momen penting dalam {domain}..."
            ]
        }
        
        # General response templates for unknown topics
        self.general_responses = [
            "Pertanyaan menarik! {topic} adalah topik kompleks yang memiliki banyak dimensi.",
            "Ini adalah topik yang menarik untuk didiskusikan. {topic} memiliki berbagai aspek penting.",
            "Saya senang Anda menanyakan tentang {topic}. Ini adalah bidang yang luas dengan banyak perspektif.",
            "Tantangan dalam memahami {topic} adalah kompleksitas dan berbagai sudut pandang yang terlibat."
        ]
        
        # Context tracking for more coherent conversations
        self.conversation_history = []
        self.max_history = 10
        
        # Confidence scoring for responses
        self.confidence_threshold = 0.6

    def identify_topic_domain(self, text):
        """Identify the main domain of the question"""
        text_lower = text.lower()
        
        domain_keywords = {
            'science': ['fisika', 'kimia', 'biologi', 'astronomi', 'ilmu', 'sains', 'science', 'physics', 'chemistry', 'biology'],
            'technology': ['teknologi', 'komputer', 'software', 'hardware', 'ai', 'artificial intelligence', 'program', 'tech', 'digital'],
            'society': ['politik', 'ekonomi', 'sosial', 'masyarakat', 'pemerintah', 'demokrasi', 'ekonomi', 'governance', 'social'],
            'culture': ['seni', 'budaya', 'filsafat', 'filosofi', 'estetika', 'art', 'culture', 'philosophy']
        }
        
        scores = defaultdict(int)
        
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[domain] += 1
        
        if scores:
            return max(scores, key=scores.get)
        return 'general'

    def identify_subtopic(self, text, domain):
        """Identify subtopic within a domain"""
        text_lower = text.lower()
        
        if domain == 'science':
            subtopics = {
                'physics': ['fisika', 'partikel', 'energi', 'gaya', 'motion', 'quantum'],
                'chemistry': ['kimia', 'reaksi', 'atom', 'molekul', 'senyawa', 'chemical'],
                'biology': ['biologi', 'dna', 'sel', 'evolusi', 'organisme', 'biological'],
                'astronomy': ['astronomi', 'bintang', 'planet', 'galaksi', 'ruang angkasa', 'space']
            }
        elif domain == 'technology':
            subtopics = {
                'ai_ml': ['ai', 'machine learning', 'neural', 'deep learning', 'algoritma', 'algorithm'],
                'programming': ['program', 'kode', 'coding', 'software', 'programming'],
                'hardware': ['hardware', 'chip', 'processor', 'komputer', 'computer']
            }
        elif domain == 'society':
            subtopics = {
                'politics': ['politik', 'pemerintah', 'demokrasi', 'pemilu', 'policy', 'governance'],
                'economics': ['ekonomi', 'uang', 'pasar', 'inflasi', 'ekonomi', 'economic'],
                'education': ['pendidikan', 'sekolah', 'universitas', 'belajar', 'education', 'learning']
            }
        elif domain == 'culture':
            subtopics = {
                'philosophy': ['filsafat', 'filosofi', 'etika', 'epistemologi', 'philosophy', 'ethics'],
                'arts': ['seni', 'lukis', 'musik', 'sastra', 'art', 'music', 'literature']
            }
        else:
            return None
            
        scores = defaultdict(int)
        
        for subtopic, keywords in subtopics.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[subtopic] += 1
        
        if scores:
            return max(scores, key=scores.get)
        return None

    def classify_question_type(self, text):
        """Classify the type of question being asked"""
        text_lower = text.lower()
        
        for qtype, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return qtype
        return 'general'

    def extract_key_entities(self, text):
        """Extract key entities from the text"""
        # Simple extraction based on common patterns
        # In a real implementation, this would use NLP libraries
        words = text.split()
        entities = []
        
        # Look for capitalized words and specific patterns
        for i, word in enumerate(words):
            # Capitalized words (potential entities)
            if word[0].isupper() and len(word) > 2:
                entities.append(word.strip('.,!?'))
            
            # Words after certain indicators
            if i > 0 and words[i-1].lower() in ['tentang', 'mengenai', 'perihal', 'about', 'regarding']:
                entities.append(word.strip('.,!?'))
        
        return entities if entities else ['topik ini']

    def generate_contextual_response(self, user_input, domain, subtopic, qtype, entities):
        """Generate a contextual response based on analysis"""
        
        # If we have specific knowledge for this domain/subtopic combination
        if domain in self.knowledge_base and subtopic in self.knowledge_base[domain]:
            specific_knowledge = random.choice(self.knowledge_base[domain][subtopic])
            if qtype in self.response_templates:
                template = random.choice(self.response_templates[qtype])
                entity_str = entities[0] if entities else 'topik ini'
                return template.format(**{entity_str.lower(): entity_str}) + " " + specific_knowledge
            else:
                return specific_knowledge
        
        # If we have general knowledge about the domain
        elif domain in ['science', 'technology', 'society', 'culture']:
            if qtype in self.response_templates:
                template = random.choice(self.response_templates[qtype])
                entity_str = entities[0] if entities else 'topik ini'
                return template.format(**{entity_str.lower(): entity_str}) + f" Ini adalah bagian dari bidang {domain}."
        
        # Fallback to general response
        else:
            general_template = random.choice(self.general_responses)
            entity_str = entities[0] if entities else 'topik ini'
            return general_template.format(topic=entity_str)

    def get_response(self, user_input):
        """Main response generation function"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Silakan ajukan pertanyaan atau sampaikan topik yang ingin Anda bahas. Saya siap memberikan respons yang informatif dan bermanfaat."
        
        # Add to conversation history
        self.conversation_history.append(('user', user_input))
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # Analyze the input
        domain = self.identify_topic_domain(user_input)
        subtopic = self.identify_subtopic(user_input, domain)
        qtype = self.classify_question_type(user_input)
        entities = self.extract_key_entities(user_input)
        
        # Generate contextual response
        response = self.generate_contextual_response(user_input, domain, subtopic, qtype, entities)
        
        # Enhance with critical thinking if applicable
        if qtype in ['causal', 'evaluation', 'solution', 'prediction']:
            critical_elements = [
                "Dari perspektif kritis, beberapa aspek penting perlu dipertimbangkan...",
                "Penting untuk memahami konteks dan asumsi yang mendasari...",
                "Beberapa pendekatan alternatif juga bisa dipertimbangkan...",
                "Implikasi dari hal ini bisa sangat luas dan kompleks..."
            ]
            response += " " + random.choice(critical_elements)
        
        # Add to history
        self.conversation_history.append(('bot', response))
        
        return response

    def chat(self):
        """Main chat loop"""
        print("🤖 Universal AI Bot - Versi Super Cerdas")
        print("=" * 50)
        print("Halo! Saya adalah AI universal yang dirancang untuk menjawab berbagai jenis pertanyaan.")
        print("Saya memiliki pengetahuan dalam berbagai bidang: sains, teknologi, sosial, budaya, dan lainnya.")
        print("Saya juga bisa menganalisis, membandingkan, mengevaluasi, dan memberikan solusi.")
        print("Ketik 'quit' untuk keluar.")
        print()
        
        while True:
            try:
                user_input = input("Anda: ").strip()
                
                # Exit condition
                if user_input.lower() in ['quit', 'exit', 'bye', 'keluar', 'berhenti']:
                    print("AI Bot: Terima kasih atas pertanyaan dan diskusi yang menarik! Sampai jumpa!")
                    break
                
                # Handle empty input
                if not user_input:
                    print("AI Bot: Silakan ajukan pertanyaan atau sampaikan topik yang ingin Anda bahas.")
                    continue
                
                # Get and print intelligent response
                response = self.get_response(user_input)
                print(f"AI Bot: {response}")
                print()
                
            except KeyboardInterrupt:
                print("\n\nAI Bot: Diskusi yang menarik! Sampai jumpa lain waktu!")
                break
            except Exception as e:
                print(f"AI Bot: Maaf, terjadi kesalahan dalam memproses pertanyaan Anda: {e}")
                print("Silakan coba pertanyaan lain.")

def main():
    """Main function to run the universal AI bot"""
    ai_bot = UniversalAIBot()
    ai_bot.chat()

if __name__ == "__main__":
    main()
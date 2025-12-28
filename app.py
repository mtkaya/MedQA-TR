"""
🏥 MedQA-TR: Türkçe Tıbbi Soru-Cevap Benchmark Demo
Hugging Face Space
"""

import gradio as gr
import json
import random
from dataclasses import dataclass
from typing import Optional, Dict, List

# ============================================
# VERİ
# ============================================

QUESTIONS = [
    {
        "id": "medqa_tr_00001",
        "question": "45 yaşında erkek hasta, 3 gündür devam eden göğüs ağrısı şikayeti ile acil servise başvuruyor. Ağrı sol kola yayılıyor ve eforla artıyor. Fizik muayenede terleme ve solukluk mevcut. EKG'de V1-V4 derivasyonlarında ST elevasyonu saptanıyor. Bu hasta için en olası tanı nedir?",
        "options": {
            "A": "Gastroözofageal reflü hastalığı",
            "B": "Akut anterior miyokard enfarktüsü",
            "C": "Pnömotoraks",
            "D": "Kostokondrit",
            "E": "Akut perikardit"
        },
        "answer": "B",
        "explanation": "V1-V4 derivasyonlarında ST elevasyonu anterior miyokard enfarktüsünü gösterir. Sol kola yayılan, eforla artan göğüs ağrısı, terleme ve solukluk tipik AKS bulgularıdır.",
        "category": "kardiyoloji",
        "difficulty": "orta"
    },
    {
        "id": "medqa_tr_00002",
        "question": "60 yaşında kadın hasta, sabah başlayan ve giderek artan nefes darlığı şikayeti ile başvuruyor. Öyküsünde 20 yıllık sigara kullanımı mevcut. Fizik muayenede ekspiryum uzamış ve bilateral ronküsler duyuluyor. SFT'de FEV1/FVC oranı %60 olarak saptanıyor. En olası tanı nedir?",
        "options": {
            "A": "Bronşiyal astım",
            "B": "Kronik obstrüktif akciğer hastalığı",
            "C": "İnterstisyel akciğer hastalığı",
            "D": "Pnömoni",
            "E": "Pulmoner emboli"
        },
        "answer": "B",
        "explanation": "Uzun süreli sigara öyküsü, ekspiryum uzaması, bilateral ronküsler ve FEV1/FVC < %70 olması KOAH tanısını destekler.",
        "category": "pulmunoloji",
        "difficulty": "orta"
    },
    {
        "id": "medqa_tr_00003",
        "question": "35 yaşında kadın hasta, son 6 aydır artan yorgunluk, kilo artışı, kabızlık ve soğuk intoleransı şikayetleri ile başvuruyor. Fizik muayenede bradikardi, kuru cilt ve pretibial ödem saptanıyor. TSH düzeyi 15 mIU/L (normal: 0.4-4.0), serbest T4 düzeyi 0.5 ng/dL (normal: 0.8-1.8) olarak ölçülüyor. Bu hasta için en uygun tedavi nedir?",
        "options": {
            "A": "Propiltiourasil",
            "B": "Levotiroksin",
            "C": "Metimazol",
            "D": "Radyoaktif iyot tedavisi",
            "E": "Tiroidektomi"
        },
        "answer": "B",
        "explanation": "Yüksek TSH ve düşük serbest T4 primer hipotiroidiyi gösterir. Tedavide levotiroksin (sentetik T4) kullanılır.",
        "category": "endokrinoloji",
        "difficulty": "orta"
    },
    {
        "id": "medqa_tr_00004",
        "question": "25 yaşında erkek hasta, son 2 gündür devam eden ateş, baş ağrısı ve ense sertliği şikayetleri ile başvuruyor. Fizik muayenede Kernig ve Brudzinski belirtileri pozitif saptanıyor. BOS incelemesinde hücre sayısı 500/mm³ (predominant nötrofil), protein 150 mg/dL, glukoz 25 mg/dL (eş zamanlı kan şekeri 100 mg/dL) olarak bulunuyor. En olası etken nedir?",
        "options": {
            "A": "Herpes simpleks virüs",
            "B": "Mycobacterium tuberculosis",
            "C": "Streptococcus pneumoniae",
            "D": "Cryptococcus neoformans",
            "E": "Enterovirus"
        },
        "answer": "C",
        "explanation": "Nötrofil predominansı, düşük BOS glukozu ve yüksek protein bakteriyel menenjiti gösterir. En sık etken Streptococcus pneumoniae'dir.",
        "category": "enfeksiyon",
        "difficulty": "zor"
    },
    {
        "id": "medqa_tr_00005",
        "question": "50 yaşında erkek hasta, son 3 aydır epigastrik ağrı ve erken doyma hissi şikayeti ile başvuruyor. Endoskopide antrum bölgesinde ülsere lezyon saptanıyor ve biyopsi alınıyor. Patoloji sonucu intestinal tip adenokarsinom olarak raporlanıyor. Helicobacter pylori testi pozitif. Bu hastanın risk faktörleri arasında aşağıdakilerden hangisi EN AZ yer alır?",
        "options": {
            "A": "Helicobacter pylori enfeksiyonu",
            "B": "Tuzlu ve tütsülenmiş gıda tüketimi",
            "C": "Gastroözofageal reflü hastalığı",
            "D": "Atrofik gastrit",
            "E": "Düşük sosyoekonomik düzey"
        },
        "answer": "C",
        "explanation": "GÖRH, özofagus adenokarsinomu için risk faktörüdür ancak mide adenokarsinomu için major risk faktörü değildir.",
        "category": "gastroenteroloji",
        "difficulty": "zor"
    },
    {
        "id": "medqa_tr_00006",
        "question": "70 yaşında erkek hasta, ani başlayan sağ kol ve bacakta güçsüzlük şikayeti ile acil servise getiriliyor. Semptomlar 2 saat önce başlamış. Nörolojik muayenede sağ hemiparezi ve dizartri saptanıyor. Kranial BT'de akut kanama bulgusu yok. Bu hasta için en uygun yaklaşım nedir?",
        "options": {
            "A": "Aspirin 300 mg başlanması",
            "B": "IV alteplaz (tPA) uygulanması",
            "C": "Mekanik trombektomi",
            "D": "Antikoagülan tedavi başlanması",
            "E": "Konservatif izlem"
        },
        "answer": "B",
        "explanation": "Semptom başlangıcından itibaren 4.5 saat içinde olan ve kontrendikasyonu olmayan akut iskemik inmede IV tPA tedavisi endikedir.",
        "category": "nöroloji",
        "difficulty": "zor"
    },
    {
        "id": "medqa_tr_00007",
        "question": "30 yaşında kadın hasta, poliüri, polidipsi ve son 1 ayda 5 kg kilo kaybı şikayetleri ile başvuruyor. Açlık kan şekeri 280 mg/dL, HbA1c %11.5 olarak saptanıyor. Anti-GAD antikoru pozitif. Bu hasta için en uygun tedavi yaklaşımı nedir?",
        "options": {
            "A": "Diyet ve egzersiz",
            "B": "Metformin monoterapisi",
            "C": "İnsülin tedavisi",
            "D": "Sülfonilüre tedavisi",
            "E": "GLP-1 agonisti"
        },
        "answer": "C",
        "explanation": "Anti-GAD pozitifliği Tip 1 diyabet veya LADA'yı düşündürür. Bu hastalarda insülin tedavisi gereklidir.",
        "category": "endokrinoloji",
        "difficulty": "orta"
    },
    {
        "id": "medqa_tr_00008",
        "question": "55 yaşında kadın hasta, son 2 haftadır sağ üst kadran ağrısı ve ateş şikayeti ile başvuruyor. Fizik muayenede sağ üst kadranda hassasiyet ve Murphy belirtisi pozitif. Laboratuvarda lökositoz ve yüksek CRP saptanıyor. Ultrasonografide safra kesesinde taş ve duvar kalınlaşması görülüyor. Bu hasta için en uygun yaklaşım nedir?",
        "options": {
            "A": "Oral antibiyotik ve ayaktan takip",
            "B": "IV antibiyotik ve erken kolesistektomi",
            "C": "Perkütan kolesistostomi",
            "D": "ERCP",
            "E": "Konservatif tedavi ve elektif cerrahi"
        },
        "answer": "B",
        "explanation": "Akut kolesistitte standart tedavi IV antibiyotik ve 72 saat içinde laparoskopik kolesistektomidir (erken kolesistektomi).",
        "category": "genel_cerrahi",
        "difficulty": "orta"
    },
    {
        "id": "medqa_tr_00009",
        "question": "40 yaşında erkek hasta, son 6 aydır ilerleyici nefes darlığı ve kuru öksürük şikayeti ile başvuruyor. Mesleki anamnezde 15 yıldır kumlama işinde çalıştığı öğreniliyor. Akciğer grafisinde üst zonlarda nodüler opasiteler ve hiler lenfadenopati saptanıyor. En olası tanı nedir?",
        "options": {
            "A": "Tüberküloz",
            "B": "Sarkoidoz",
            "C": "Silikozis",
            "D": "Asbestoz",
            "E": "Hipersensitivite pnömonisi"
        },
        "answer": "C",
        "explanation": "Kumlama işinde çalışma öyküsü (silika maruziyeti), üst zon predominansı ve nodüler opasiteler silikozis için tipiktir.",
        "category": "pulmunoloji",
        "difficulty": "zor"
    },
    {
        "id": "medqa_tr_00010",
        "question": "28 yaşında kadın hasta, son 1 yıldır adet düzensizliği, kilo artışı ve yüzde akne şikayetleri ile başvuruyor. Fizik muayenede hirsutizm ve akantozis nigrikans saptanıyor. Pelvik ultrasonografide her iki overde çok sayıda küçük folikül görülüyor. Bu hasta için tanısal testler arasında aşağıdakilerden hangisi EN ÖNEMLİ değildir?",
        "options": {
            "A": "Serbest testosteron düzeyi",
            "B": "LH/FSH oranı",
            "C": "Prolaktin düzeyi",
            "D": "CA-125 düzeyi",
            "E": "Açlık insülin düzeyi"
        },
        "answer": "D",
        "explanation": "Bulgular PKOS'u düşündürür. CA-125 over kanseri taramasında kullanılır, PKOS tanısında yeri yoktur.",
        "category": "jinekoloji",
        "difficulty": "orta"
    }
]

# Kategori renkleri
CATEGORY_COLORS = {
    "kardiyoloji": "🫀",
    "pulmunoloji": "🫁",
    "gastroenteroloji": "🔬",
    "nöroloji": "🧠",
    "endokrinoloji": "⚗️",
    "enfeksiyon": "🦠",
    "genel_cerrahi": "🔪",
    "jinekoloji": "👩‍⚕️",
    "dahiliye_genel": "🏥"
}

DIFFICULTY_LABELS = {
    "kolay": "🟢 Kolay",
    "orta": "🟡 Orta",
    "zor": "🔴 Zor",
    "uzman": "⚫ Uzman"
}

# ============================================
# UYGULAMA DURUMU
# ============================================

class QuizState:
    def __init__(self):
        self.current_question = None
        self.score = 0
        self.total = 0
        self.answered = False
        self.history = []
    
    def reset(self):
        self.score = 0
        self.total = 0
        self.history = []
        self.answered = False

state = QuizState()

# ============================================
# FONKSİYONLAR
# ============================================

def get_random_question(category_filter="Tümü"):
    """Rastgele soru getir"""
    if category_filter == "Tümü":
        available = QUESTIONS
    else:
        available = [q for q in QUESTIONS if q["category"] == category_filter]
    
    if not available:
        available = QUESTIONS
    
    return random.choice(available)

def format_question(q):
    """Soruyu formatla"""
    emoji = CATEGORY_COLORS.get(q["category"], "📋")
    difficulty = DIFFICULTY_LABELS.get(q["difficulty"], q["difficulty"])
    
    text = f"""### {emoji} {q['category'].upper()} | {difficulty}

---

**{q['question']}**

---

"""
    for key, value in q["options"].items():
        text += f"**{key}.** {value}\n\n"
    
    return text

def load_new_question(category):
    """Yeni soru yükle"""
    state.current_question = get_random_question(category)
    state.answered = False
    
    question_text = format_question(state.current_question)
    
    return (
        question_text,
        gr.update(visible=True, interactive=True),  # choices
        gr.update(visible=True, interactive=True),  # submit btn
        gr.update(value="", visible=False),         # result
        gr.update(visible=False),                   # explanation
        gr.update(visible=False),                   # next btn
    )

def check_answer(selected):
    """Cevabı kontrol et"""
    if not selected or state.answered:
        return (
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
        )
    
    state.answered = True
    state.total += 1
    
    correct = state.current_question["answer"]
    is_correct = selected[0] == correct
    
    if is_correct:
        state.score += 1
        result_text = f"""### ✅ DOĞRU!

**Seçtiğiniz:** {selected}

**Skor:** {state.score}/{state.total} ({100*state.score//state.total}%)
"""
        result_color = "green"
    else:
        result_text = f"""### ❌ YANLIŞ!

**Seçtiğiniz:** {selected}
**Doğru Cevap:** {correct}

**Skor:** {state.score}/{state.total} ({100*state.score//state.total}%)
"""
        result_color = "red"
    
    explanation = f"""### 📚 Açıklama

{state.current_question['explanation']}
"""
    
    return (
        gr.update(interactive=False),              # choices
        gr.update(visible=False),                  # submit btn
        gr.update(value=result_text, visible=True), # result
        gr.update(value=explanation, visible=True), # explanation
        gr.update(visible=True),                   # next btn
    )

def reset_quiz():
    """Quiz'i sıfırla"""
    state.reset()
    return f"**Skor:** 0/0"

def get_score():
    if state.total == 0:
        return "**Skor:** 0/0"
    return f"**Skor:** {state.score}/{state.total} ({100*state.score//state.total}%)"

def get_dataset_info():
    """Dataset bilgilerini göster"""
    categories = {}
    difficulties = {}
    
    for q in QUESTIONS:
        cat = q["category"]
        diff = q["difficulty"]
        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    info = f"""## 📊 MedQA-TR Dataset İstatistikleri

**Toplam Soru:** {len(QUESTIONS)}

### Kategoriler
"""
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        emoji = CATEGORY_COLORS.get(cat, "📋")
        info += f"- {emoji} **{cat}**: {count} soru\n"
    
    info += "\n### Zorluk Dağılımı\n"
    for diff, count in difficulties.items():
        label = DIFFICULTY_LABELS.get(diff, diff)
        info += f"- {label}: {count} soru\n"
    
    info += """

---

### 🔗 Bağlantılar

- 📦 [Dataset](https://huggingface.co/datasets/tugrulkaya/MedQA-TR)
- 💻 [GitHub](https://github.com/mtkaya)
- 🤗 [Hugging Face](https://huggingface.co/tugrulkaya)

### 📝 Atıf

```bibtex
@dataset{medqa_tr_2024,
  author = {Kaya, Mehmet Tuğrul},
  title = {MedQA-TR: Turkish Medical QA Benchmark},
  year = {2024},
  publisher = {Hugging Face}
}
```
"""
    return info

def explore_questions():
    """Tüm soruları listele"""
    text = "## 📋 Tüm Sorular\n\n"
    
    for i, q in enumerate(QUESTIONS, 1):
        emoji = CATEGORY_COLORS.get(q["category"], "📋")
        diff = DIFFICULTY_LABELS.get(q["difficulty"], q["difficulty"])
        
        text += f"""### {i}. {emoji} {q['category']} | {diff}

**{q['question'][:150]}...**

<details>
<summary>Seçenekleri Göster</summary>

"""
        for key, value in q["options"].items():
            if key == q["answer"]:
                text += f"- **{key}. {value}** ✅\n"
            else:
                text += f"- {key}. {value}\n"
        
        text += f"\n**Açıklama:** {q['explanation']}\n\n</details>\n\n---\n\n"
    
    return text

# ============================================
# GRADIO ARAYÜZÜ
# ============================================

CUSTOM_CSS = """
.container {
    max-width: 900px;
    margin: auto;
}
.question-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
}
.score-box {
    background: #f0f9ff;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
}
.correct {
    background: #d4edda;
    border: 2px solid #28a745;
    border-radius: 10px;
    padding: 15px;
}
.incorrect {
    background: #f8d7da;
    border: 2px solid #dc3545;
    border-radius: 10px;
    padding: 15px;
}
footer {
    text-align: center;
    padding: 20px;
    color: #666;
}
"""

with gr.Blocks(title="MedQA-TR") as demo:
    
    gr.Markdown("""
# 🏥 MedQA-TR: Türkçe Tıbbi Soru-Cevap Benchmark'ı

Türkçe tıbbi bilginizi test edin! TUS formatında hazırlanmış sorularla kendinizi deneyin.

---
""")
    
    with gr.Tabs():
        # ============================================
        # TAB 1: QUIZ
        # ============================================
        with gr.TabItem("🎯 Quiz"):
            with gr.Row():
                with gr.Column(scale=3):
                    category_dropdown = gr.Dropdown(
                        choices=["Tümü"] + list(set(q["category"] for q in QUESTIONS)),
                        value="Tümü",
                        label="📁 Kategori Filtresi"
                    )
                with gr.Column(scale=1):
                    score_display = gr.Markdown("**Skor:** 0/0")
                    reset_btn = gr.Button("🔄 Sıfırla", size="sm")
            
            gr.Markdown("---")
            
            question_display = gr.Markdown("*Başlamak için 'Yeni Soru' butonuna tıklayın*")
            
            answer_radio = gr.Radio(
                choices=["A", "B", "C", "D", "E"],
                label="Cevabınız",
                visible=False,
                interactive=True
            )
            
            submit_btn = gr.Button("✅ Cevabı Kontrol Et", variant="primary", visible=False)
            
            result_display = gr.Markdown(visible=False)
            explanation_display = gr.Markdown(visible=False)
            
            next_btn = gr.Button("➡️ Sonraki Soru", variant="secondary", visible=False)
            
            start_btn = gr.Button("🎲 Yeni Soru", variant="primary", size="lg")
            
            # Event handlers
            start_btn.click(
                fn=load_new_question,
                inputs=[category_dropdown],
                outputs=[question_display, answer_radio, submit_btn, result_display, explanation_display, next_btn]
            )
            
            next_btn.click(
                fn=load_new_question,
                inputs=[category_dropdown],
                outputs=[question_display, answer_radio, submit_btn, result_display, explanation_display, next_btn]
            )
            
            submit_btn.click(
                fn=check_answer,
                inputs=[answer_radio],
                outputs=[answer_radio, submit_btn, result_display, explanation_display, next_btn]
            ).then(
                fn=get_score,
                outputs=[score_display]
            )
            
            reset_btn.click(
                fn=reset_quiz,
                outputs=[score_display]
            )
        
        # ============================================
        # TAB 2: DATASET BİLGİSİ
        # ============================================
        with gr.TabItem("📊 Dataset"):
            dataset_info = gr.Markdown(get_dataset_info())
        
        # ============================================
        # TAB 3: TÜM SORULAR
        # ============================================
        with gr.TabItem("📋 Tüm Sorular"):
            all_questions = gr.Markdown(explore_questions())
    
    gr.Markdown("""
---

<center>

**MedQA-TR** | Geliştirici: [Mehmet Tuğrul Kaya](https://huggingface.co/tugrulkaya) | 2024

⚠️ *Bu uygulama eğitim amaçlıdır. Gerçek tıbbi kararlar için uzman hekime danışın.*

</center>
""")

# ============================================
# ÇALIŞTIR
# ============================================

if __name__ == "__main__":
    demo.launch()

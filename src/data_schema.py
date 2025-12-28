"""
MedQA-TR: Türkçe Tıbbi Soru-Cevap Benchmark'ı
Veri Şeması ve Yardımcı Fonksiyonlar
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import json

class Difficulty(str, Enum):
    EASY = "kolay"
    MEDIUM = "orta"
    HARD = "zor"
    EXPERT = "uzman"

class QuestionType(str, Enum):
    MCQA = "mcqa"
    OPEN = "open"
    BOOLEAN = "boolean"
    EXPLAIN = "explain"

MEDICAL_CATEGORIES = [
    "kardiyoloji", "nöroloji", "gastroenteroloji", "pulmunoloji",
    "endokrinoloji", "nefroloji", "hematoloji", "romatoloji",
    "enfeksiyon", "dermatoloji", "psikiyatri", "pediatri",
    "jinekoloji", "üroloji", "ortopedi", "genel_cerrahi",
    "acil_tıp", "farmakoloji", "patoloji", "radyoloji",
    "anatomi", "fizyoloji", "biyokimya", "mikrobiyoloji",
    "halk_sağlığı", "dahiliye_genel"
]

@dataclass
class MedQAItem:
    """Tek bir MedQA-TR örneği"""
    id: str
    question: str
    question_type: str
    category: str
    difficulty: str
    answer: str
    options: Optional[Dict[str, str]] = None
    explanation: Optional[str] = None
    source: str = ""
    source_url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    verified: bool = False
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def validate(self) -> List[str]:
        errors = []
        if len(self.question) < 20:
            errors.append("Soru çok kısa")
        if self.question_type == "mcqa" and not self.options:
            errors.append("MCQA için seçenekler gerekli")
        if self.question_type == "mcqa" and self.options:
            if self.answer not in self.options:
                errors.append("Cevap seçeneklerde yok")
        return errors

def create_sample_data() -> List[dict]:
    """Örnek TUS benzeri sorular oluştur"""
    samples = [
        MedQAItem(
            id="medqa_tr_00001",
            question="45 yaşında erkek hasta, 3 gündür devam eden göğüs ağrısı şikayeti ile acil servise başvuruyor. Ağrı sol kola yayılıyor ve eforla artıyor. Fizik muayenede terleme ve solukluk mevcut. EKG'de V1-V4 derivasyonlarında ST elevasyonu saptanıyor. Bu hasta için en olası tanı nedir?",
            question_type=QuestionType.MCQA.value,
            category="kardiyoloji",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Gastroözofageal reflü hastalığı",
                "B": "Akut anterior miyokard enfarktüsü",
                "C": "Pnömotoraks",
                "D": "Kostokondrit",
                "E": "Akut perikardit"
            },
            answer="B",
            explanation="V1-V4 derivasyonlarında ST elevasyonu anterior miyokard enfarktüsünü gösterir. Sol kola yayılan, eforla artan göğüs ağrısı, terleme ve solukluk tipik AKS bulgularıdır.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00002",
            question="60 yaşında kadın hasta, sabah başlayan ve giderek artan nefes darlığı şikayeti ile başvuruyor. Öyküsünde 20 yıllık sigara kullanımı mevcut. Fizik muayenede ekspiryum uzamış ve bilateral ronküsler duyuluyor. SFT'de FEV1/FVC oranı %60 olarak saptanıyor. En olası tanı nedir?",
            question_type=QuestionType.MCQA.value,
            category="pulmunoloji",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Bronşiyal astım",
                "B": "Kronik obstrüktif akciğer hastalığı",
                "C": "İnterstisyel akciğer hastalığı",
                "D": "Pnömoni",
                "E": "Pulmoner emboli"
            },
            answer="B",
            explanation="Uzun süreli sigara öyküsü, ekspiryum uzaması, bilateral ronküsler ve FEV1/FVC < %70 olması KOAH tanısını destekler.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00003",
            question="35 yaşında kadın hasta, son 6 aydır artan yorgunluk, kilo artışı, kabızlık ve soğuk intoleransı şikayetleri ile başvuruyor. Fizik muayenede bradikardi, kuru cilt ve pretibial ödem saptanıyor. TSH düzeyi 15 mIU/L (normal: 0.4-4.0), serbest T4 düzeyi 0.5 ng/dL (normal: 0.8-1.8) olarak ölçülüyor. Bu hasta için en uygun tedavi nedir?",
            question_type=QuestionType.MCQA.value,
            category="endokrinoloji",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Propiltiourasil",
                "B": "Levotiroksin",
                "C": "Metimazol",
                "D": "Radyoaktif iyot tedavisi",
                "E": "Tiroidektomi"
            },
            answer="B",
            explanation="Yüksek TSH ve düşük serbest T4 primer hipotiroidiyi gösterir. Tedavide levotiroksin (sentetik T4) kullanılır.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00004",
            question="25 yaşında erkek hasta, son 2 gündür devam eden ateş, baş ağrısı ve ense sertliği şikayetleri ile başvuruyor. Fizik muayenede Kernig ve Brudzinski belirtileri pozitif saptanıyor. BOS incelemesinde hücre sayısı 500/mm³ (predominant nötrofil), protein 150 mg/dL, glukoz 25 mg/dL (eş zamanlı kan şekeri 100 mg/dL) olarak bulunuyor. En olası etken nedir?",
            question_type=QuestionType.MCQA.value,
            category="enfeksiyon",
            difficulty=Difficulty.HARD.value,
            options={
                "A": "Herpes simpleks virüs",
                "B": "Mycobacterium tuberculosis",
                "C": "Streptococcus pneumoniae",
                "D": "Cryptococcus neoformans",
                "E": "Enterovirus"
            },
            answer="C",
            explanation="Nötrofil predominansı, düşük BOS glukozu ve yüksek protein bakteriyel menenjiti gösterir. En sık etken Streptococcus pneumoniae'dir.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00005",
            question="50 yaşında erkek hasta, son 3 aydır epigastrik ağrı ve erken doyma hissi şikayeti ile başvuruyor. Endoskopide antrum bölgesinde ülsere lezyon saptanıyor ve biyopsi alınıyor. Patoloji sonucu intestinal tip adenokarsinom olarak raporlanıyor. Helicobacter pylori testi pozitif. Bu hastanın risk faktörleri arasında aşağıdakilerden hangisi EN AZ yer alır?",
            question_type=QuestionType.MCQA.value,
            category="gastroenteroloji",
            difficulty=Difficulty.HARD.value,
            options={
                "A": "Helicobacter pylori enfeksiyonu",
                "B": "Tuzlu ve tütsülenmiş gıda tüketimi",
                "C": "Gastroözofageal reflü hastalığı",
                "D": "Atrofik gastrit",
                "E": "Düşük sosyoekonomik düzey"
            },
            answer="C",
            explanation="GÖRH, özofagus adenokarsinomu için risk faktörüdür ancak mide adenokarsinomu için major risk faktörü değildir. H. pylori, tuzlu gıdalar, atrofik gastrit ve düşük sosyoekonomik düzey mide kanseri risk faktörleridir.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00006",
            question="70 yaşında erkek hasta, ani başlayan sağ kol ve bacakta güçsüzlük şikayeti ile acil servise getiriliyor. Semptomlar 2 saat önce başlamış. Nörolojik muayenede sağ hemiparezi ve dizartri saptanıyor. Kranial BT'de akut kanama bulgusu yok. Bu hasta için en uygun yaklaşım nedir?",
            question_type=QuestionType.MCQA.value,
            category="nöroloji",
            difficulty=Difficulty.HARD.value,
            options={
                "A": "Aspirin 300 mg başlanması",
                "B": "IV alteplaz (tPA) uygulanması",
                "C": "Mekanik trombektomi",
                "D": "Antikoagülan tedavi başlanması",
                "E": "Konservatif izlem"
            },
            answer="B",
            explanation="Semptom başlangıcından itibaren 4.5 saat içinde olan ve kontrendikasyonu olmayan akut iskemik inmede IV tPA tedavisi endikedir. 2 saatlik semptom süresi tedavi penceresinde.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00007",
            question="30 yaşında kadın hasta, poliüri, polidipsi ve son 1 ayda 5 kg kilo kaybı şikayetleri ile başvuruyor. Açlık kan şekeri 280 mg/dL, HbA1c %11.5 olarak saptanıyor. Anti-GAD antikoru pozitif. Bu hasta için en uygun tedavi yaklaşımı nedir?",
            question_type=QuestionType.MCQA.value,
            category="endokrinoloji",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Diyet ve egzersiz",
                "B": "Metformin monoterapisi",
                "C": "İnsülin tedavisi",
                "D": "Sülfonilüre tedavisi",
                "E": "GLP-1 agonisti"
            },
            answer="C",
            explanation="Anti-GAD pozitifliği Tip 1 diyabet veya LADA'yı düşündürür. Bu hastalarda insülin tedavisi gereklidir, oral antidiyabetikler etkisizdir.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00008",
            question="55 yaşında kadın hasta, son 2 haftadır sağ üst kadran ağrısı ve ateş şikayeti ile başvuruyor. Fizik muayenede sağ üst kadranda hassasiyet ve Murphy belirtisi pozitif. Laboratuvarda lökositoz ve yüksek CRP saptanıyor. Ultrasonografide safra kesesinde taş ve duvar kalınlaşması görülüyor. Bu hasta için en uygun yaklaşım nedir?",
            question_type=QuestionType.MCQA.value,
            category="genel_cerrahi",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Oral antibiyotik ve ayaktan takip",
                "B": "IV antibiyotik ve erken kolesistektomi",
                "C": "Perkütan kolesistostomi",
                "D": "ERCP",
                "E": "Konservatif tedavi ve elektif cerrahi"
            },
            answer="B",
            explanation="Akut kolesistitte standart tedavi IV antibiyotik ve 72 saat içinde laparoskopik kolesistektomidir (erken kolesistektomi).",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00009",
            question="40 yaşında erkek hasta, son 6 aydır ilerleyici nefes darlığı ve kuru öksürük şikayeti ile başvuruyor. Mesleki anamnezde 15 yıldır kumlama işinde çalıştığı öğreniliyor. Akciğer grafisinde üst zonlarda nodüler opasiteler ve hiler lenfadenopati saptanıyor. En olası tanı nedir?",
            question_type=QuestionType.MCQA.value,
            category="pulmunoloji",
            difficulty=Difficulty.HARD.value,
            options={
                "A": "Tüberküloz",
                "B": "Sarkoidoz",
                "C": "Silikozis",
                "D": "Asbestoz",
                "E": "Hipersensitivite pnömonisi"
            },
            answer="C",
            explanation="Kumlama işinde çalışma öyküsü (silika maruziyeti), üst zon predominansı ve nodüler opasiteler silikozis için tipiktir.",
            source="manual_creation"
        ),
        MedQAItem(
            id="medqa_tr_00010",
            question="28 yaşında kadın hasta, son 1 yıldır adet düzensizliği, kilo artışı ve yüzde akne şikayetleri ile başvuruyor. Fizik muayenede hirsutizm ve akantozis nigrikans saptanıyor. Pelvik ultrasonografide her iki overde çok sayıda küçük folikül görülüyor. Bu hasta için tanısal testler arasında aşağıdakilerden hangisi EN ÖNEMLİ değildir?",
            question_type=QuestionType.MCQA.value,
            category="jinekoloji",
            difficulty=Difficulty.MEDIUM.value,
            options={
                "A": "Serbest testosteron düzeyi",
                "B": "LH/FSH oranı",
                "C": "Prolaktin düzeyi",
                "D": "CA-125 düzeyi",
                "E": "Açlık insülin düzeyi"
            },
            answer="D",
            explanation="Bulgular PKOS'u düşündürür. CA-125 over kanseri taramasında kullanılır, PKOS tanısında yeri yoktur. Diğer testler PKOS değerlendirmesinde önemlidir.",
            source="manual_creation"
        )
    ]
    
    return [s.to_dict() for s in samples]

if __name__ == "__main__":
    samples = create_sample_data()
    print(f"✅ {len(samples)} örnek oluşturuldu")
    
    # JSON olarak kaydet
    import os
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "manual_samples.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)
    print(f"💾 Kaydedildi: {output_path}")

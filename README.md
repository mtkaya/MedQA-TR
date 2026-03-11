# MedQA-TR: Türkçe Tıbbi Soru-Cevap Benchmark'ı

[![Hugging Face Space](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/tugrulkaya/MedQA-TR)
[![Dataset](https://img.shields.io/badge/🤗%20Dataset-MedQA--TR-yellow)](https://huggingface.co/datasets/tugrulkaya/MedQA-TR)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

Türkçe tıbbi soru-cevap sistemleri için oluşturulmuş ilk kapsamlı benchmark dataset'i ve interaktif demo uygulaması.

## Proje Hakkında

MedQA-TR, TUS (Tıpta Uzmanlık Sınavı) formatında hazırlanmış Türkçe tıbbi sorular içeren bir benchmark'tır. Türkçe tıbbi NLP araştırmaları için standart bir değerlendirme seti oluşturmayı hedefler.

### Özellikler

- 🎯 **Interaktif Quiz**: Rastgele sorularla kendinizi test edin
- 📁 **9 Tıbbi Kategori**: Kardiyoloji, Nöroloji, Endokrinoloji ve daha fazlası
- ✅ **Detaylı Açıklamalar**: Her sorunun ardından öğretici açıklamalar
- 📊 **Skor Takibi**: Performansınızı anlık olarak görün
- 🤗 **HuggingFace Entegrasyonu**: Dataset ve Space olarak erişilebilir

## Dataset İstatistikleri

| Özellik | Değer |
|---------|-------|
| Toplam Soru | 10 (v0.1) |
| Format | Çoktan Seçmeli (5 şık) |
| Kategoriler | 9 tıbbi branş |
| Zorluk Seviyeleri | Kolay / Orta / Zor |
| Dil | Türkçe |

## Kategoriler

| Emoji | Kategori | Açıklama |
|-------|----------|----------|
| 🫀 | Kardiyoloji | Kalp ve damar hastalıkları |
| 🫁 | Pulmunoloji | Solunum sistemi hastalıkları |
| 🧠 | Nöroloji | Sinir sistemi hastalıkları |
| ⚗️ | Endokrinoloji | Hormon ve metabolizma |
| 🔬 | Gastroenteroloji | Sindirim sistemi |
| 🦠 | Enfeksiyon | Bulaşıcı hastalıklar |
| 🔪 | Genel Cerrahi | Cerrahi durumlar |
| 👩‍⚕️ | Jinekoloji | Kadın hastalıkları |
| 🏥 | Dahiliye | Genel iç hastalıkları |

## Kurulum

```bash
# Repo'yu klonla
git clone https://github.com/mtkaya/MedQA-TR.git
cd MedQA-TR

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

Tarayıcıda `http://localhost:7860` adresini aç.

## Proje Yapısı

```
MedQA-TR/
├── app.py                 # Gradio demo uygulaması
├── requirements.txt       # Python bağımlılıkları
├── README.md             
├── data/
│   ├── raw/
│   │   └── manual_samples.json    # Ham veri
│   └── processed/
│       └── hf_dataset/            # HuggingFace formatı
├── src/
│   ├── data_schema.py            # Veri şeması
│   └── create_hf_dataset.py      # Dataset oluşturma
└── upload_to_hub.py              # HF yükleme scripti
```

## Kullanım

### Python ile Dataset Kullanımı

```python
from datasets import load_dataset
import json

# Dataset'i yükle
dataset = load_dataset("tugrulkaya/MedQA-TR")

# Örnek bir soruya bak
example = dataset['train'][0]
print(f"Soru: {example['question']}")

# Seçenekleri parse et
options = json.loads(example['options'])
for key, value in options.items():
    marker = "✅" if key == example['answer'] else "  "
    print(f"{marker} {key}: {value}")
```

### Veri Formatı

```json
{
  "id": "medqa_tr_00001",
  "question": "45 yaşında erkek hasta...",
  "question_type": "mcqa",
  "category": "kardiyoloji",
  "difficulty": "orta",
  "options": {"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."},
  "answer": "B",
  "explanation": "Detaylı açıklama...",
  "verified": false
}
```

## ️ Yol Haritası

- [x] v0.1 - İlk versiyon (10 manuel soru)
- [ ] v0.2 - MedQA çevirisi ekleme (100+ soru)
- [ ] v0.3 - TUS soru bankası entegrasyonu
- [ ] v0.4 - Uzman doğrulaması
- [ ] v1.0 - Tam benchmark (1000+ soru)

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/YeniOzellik`)
5. Pull Request açın

## Lisans

Bu proje [Apache 2.0](LICENSE) lisansı altında yayınlanmaktadır.

## Geliştirici

**Mehmet Tuğrul Kaya**

- 🤗 HuggingFace: [@tugrulkaya](https://huggingface.co/tugrulkaya)
- 💻 GitHub: [@mtkaya](https://github.com/mtkaya)

## Atıf

```bibtex
@misc{medqa_tr_2024,
  author = {Kaya, Mehmet Tuğrul},
  title = {MedQA-TR: Turkish Medical Question Answering Benchmark},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/mtkaya/MedQA-TR}
}
```

## Bağlantılar

- 🌐 [Live Demo](https://huggingface.co/spaces/tugrulkaya/MedQA-TR)
- 📦 [HuggingFace Dataset](https://huggingface.co/datasets/tugrulkaya/MedQA-TR)

---

⚠️ **Feragatname**: Bu proje eğitim ve araştırma amaçlıdır. Gerçek tıbbi kararlar için uzman hekime danışın.

<p align="center">Made with ❤️ for Turkish NLP Community</p>

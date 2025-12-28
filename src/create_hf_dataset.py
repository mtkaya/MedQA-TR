"""
MedQA-TR: Hugging Face'e Dataset Yükleme
"""

import json
import os
from datasets import Dataset, DatasetDict, Features, Value

# Veriyi yükle
data_path = "/home/claude/MedQA-TR/data/raw/manual_samples.json"
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"📊 Yüklenen veri: {len(data)} örnek")

# Options'ı JSON string'e çevir (HF Dataset için)
for item in data:
    if isinstance(item.get('options'), dict):
        item['options'] = json.dumps(item['options'], ensure_ascii=False)
    if item.get('explanation') is None:
        item['explanation'] = ""
    if item.get('source_url') is None:
        item['source_url'] = ""

# Dataset oluştur
dataset = Dataset.from_list(data)

print(f"✅ Dataset oluşturuldu")
print(f"   Kolonlar: {dataset.column_names}")
print(f"   Örnek sayısı: {len(dataset)}")

# Train/validation/test split (80/10/10)
# Küçük veri seti olduğu için manuel bölüyoruz
train_size = int(len(dataset) * 0.8)
val_size = int(len(dataset) * 0.1)

train_dataset = dataset.select(range(train_size))
val_dataset = dataset.select(range(train_size, train_size + val_size))
test_dataset = dataset.select(range(train_size + val_size, len(dataset)))

dataset_dict = DatasetDict({
    'train': train_dataset,
    'validation': val_dataset,
    'test': test_dataset
})

print(f"\n📁 Dataset Split:")
print(f"   Train: {len(dataset_dict['train'])}")
print(f"   Validation: {len(dataset_dict['validation'])}")
print(f"   Test: {len(dataset_dict['test'])}")

# Lokal kaydet
output_dir = "/home/claude/MedQA-TR/data/processed/hf_dataset"
dataset_dict.save_to_disk(output_dir)
print(f"\n💾 Lokal kayıt: {output_dir}")

# Örnek veri göster
print("\n📋 Örnek veri:")
print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500] + "...")

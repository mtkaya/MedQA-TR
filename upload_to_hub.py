"""
MedQA-TR: Hugging Face Hub'a Yükleme
=====================================

KULLANIM:
1. HF Token al: https://huggingface.co/settings/tokens (Write yetkili)
2. Token'ı aşağıya yapıştır
3. Script'i çalıştır: python upload_to_hub.py
"""

from huggingface_hub import HfApi, login, create_repo
from datasets import load_from_disk
import os

# ============================================
# ⚠️ TOKEN'INI BURAYA YAPISTIR
# ============================================
HF_TOKEN = ""  # <-- hf_xxxxxxxxxxxx formatında token'ını buraya yaz
# ============================================

REPO_NAME = "MedQA-TR"
PRIVATE = False  # True yaparak private repo oluşturabilirsin

def main():
    if not HF_TOKEN:
        print("❌ HATA: HF_TOKEN boş!")
        print("   1. https://huggingface.co/settings/tokens adresine git")
        print("   2. 'New token' → 'Write' yetkisi ver")
        print("   3. Token'ı kopyala ve bu script'e yapıştır")
        return
    
    # Login
    print("🔑 Hugging Face'e giriş yapılıyor...")
    login(token=HF_TOKEN)
    
    api = HfApi()
    user_info = api.whoami()
    username = user_info['name']
    print(f"✅ Giriş başarılı: {username}")
    
    repo_id = f"{username}/{REPO_NAME}"
    
    # Dataset'i yükle
    print("\n📂 Dataset yükleniyor...")
    dataset_path = "/home/claude/MedQA-TR/data/processed/hf_dataset"
    dataset = load_from_disk(dataset_path)
    print(f"   Train: {len(dataset['train'])} örnek")
    print(f"   Validation: {len(dataset['validation'])} örnek")
    print(f"   Test: {len(dataset['test'])} örnek")
    
    # Hub'a yükle
    print(f"\n📤 Hub'a yükleniyor: {repo_id}")
    dataset.push_to_hub(
        repo_id,
        private=PRIVATE,
        token=HF_TOKEN
    )
    
    print(f"\n✅ Dataset yüklendi!")
    print(f"🔗 https://huggingface.co/datasets/{repo_id}")
    
    # README'yi yükle
    print("\n📝 README yükleniyor...")
    readme_path = "/home/claude/MedQA-TR/README.md"
    if os.path.exists(readme_path):
        api.upload_file(
            path_or_fileobj=readme_path,
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
            token=HF_TOKEN
        )
        print("✅ README yüklendi!")
    
    print("\n" + "=" * 50)
    print("🎉 TAMAMLANDI!")
    print(f"🔗 Dataset: https://huggingface.co/datasets/{repo_id}")
    print("=" * 50)

if __name__ == "__main__":
    main()

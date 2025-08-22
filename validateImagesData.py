import os

# ===== CONFIGURAÇÃO =====
txt_file = 'car_image_list.txt'  # arquivo original com train/validation/test
images_folder = './images'       # pasta onde estão train/, validation/, test/
# =========================

# Lê o txt e organiza os IDs por split
expected = {'train': set(), 'validation': set(), 'test': set()}
with open(txt_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        split, image_id = line.split('/')
        expected[split].add(f"{image_id}.jpg")

# Função auxiliar para checar cada pasta
def check_folder(split):
    folder = os.path.join(images_folder, split)
    if not os.path.exists(folder):
        print(f"❌ Pasta {folder} não encontrada.")
        return
    
    files = set(os.listdir(folder))
    missing = expected[split] - files
    extra = files - expected[split]

    print(f"\n📂 {split.upper()}:")
    print(f" - Esperado: {len(expected[split])} imagens")
    print(f" - Encontrado: {len(files)} imagens")
    print(f" - Faltando: {len(missing)}")
    print(f" - Extras: {len(extra)}")

    if missing:
        print("   -> Faltando:", list(missing)[:10], "...")
    if extra:
        print("   -> Extras:", list(extra)[:10], "...")

# Rodar para cada split
for split in ['train', 'validation', 'test']:
    check_folder(split)
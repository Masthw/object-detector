import os
import shutil
import subprocess

# ===== CONFIGURAÇÃO =====
txt_file = 'car_image_list.txt'      # arquivo com todas as imagens (train/validation/validation)
download_folder = './images'          # pasta onde as imagens serão baixadas
max_validation = 500                  # número máximo de imagens de validation a baixar
validation_file = 'validation_image_list.txt'  # arquivo temporário para o downloader
# ========================

# 1️⃣ Cria arquivo temporário apenas com as primeiras 500 imagens de validation
with open(txt_file, 'r') as f, open(validation_file, 'w') as out_f:
    count = 0
    for line in f:
        line = line.strip()         # remove espaços e quebras de linha
        if not line:                # ignora linhas vazias
            continue
        if line.startswith('validation/'):
            out_f.write(line + '\n')
            count += 1
            if count >= max_validation:
                break

print(f"Arquivo {validation_file} criado com {count} imagens de validation.")

# 2️⃣ Chama o downloader.py para baixar as imagens
subprocess.run([
    'python', 'downloader.py',
    validation_file,
    '--download_folder', download_folder,
    '--num_processes', '5'
])

print("Download das imagens concluído.")

# 3️⃣ Organiza as imagens dentro da pasta images/validation/
validation_folder = os.path.join(download_folder, 'validation')
if not os.path.exists(validation_folder):
    os.makedirs(validation_folder)

with open(validation_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        split, image_id = line.split('/')
        src = os.path.join(download_folder, f'{image_id}.jpg')
        dst = os.path.join(validation_folder, f'{image_id}.jpg')
        if os.path.exists(src):
            shutil.move(src, dst)

print(f"Imagens organizadas em {validation_folder}.")

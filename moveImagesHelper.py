import os
import shutil

# Pastas fontes
all_images = './images_all'           # car_image
validation_images = './validation_image'
test_images = './test_image'

# Pasta final
images_folder = './images'

# Arquivo com os splits
txt_file = 'car_image_list.txt'

# Cria pastas finais
for split in ['train', 'validation', 'test']:
    os.makedirs(os.path.join(images_folder, split), exist_ok=True)

# Move imagens de train
with open(txt_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        split, image_id = line.split('/')
        # Ignora validation/test, que já tem pasta própria
        if split == 'train':
            src = os.path.join(all_images, f'{image_id}.jpg')
            dst = os.path.join(images_folder, split, f'{image_id}.jpg')
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.move(src, dst)

# Move imagens de validation
for img in os.listdir(validation_images):
    src = os.path.join(validation_images, img)
    dst = os.path.join(images_folder, 'validation', img)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)

# Move imagens de test
for img in os.listdir(test_images):
    src = os.path.join(test_images, img)
    dst = os.path.join(images_folder, 'test', img)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.move(src, dst)

print("Organização concluída!")

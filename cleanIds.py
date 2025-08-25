import os
import glob

BASE = "dataset"  # ajuste se precisar
LABEL_ROOT = os.path.join(BASE, "labels")
SPLITS = ("train", "validation", "test")

OLD_TO_NEW = {"570": "0"}   # mapeia Car do Open Images -> índice 0 do seu dataset
KEEP = {"0"}                # manter apenas a classe 0 (Car)

total_files = 0
changed_files = 0
removed_lines = 0

for split in SPLITS:
    d = os.path.join(LABEL_ROOT, split)
    if not os.path.isdir(d):
        continue
    for txt in glob.glob(os.path.join(d, "*.txt")):
        total_files += 1
        with open(txt, "r") as f:
            lines = f.readlines()

        new_lines = []
        file_removed = 0
        file_changed = False

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            # 1) converte ids antigos -> novos (ex.: 570 -> 0)
            if parts[0] in OLD_TO_NEW:
                parts[0] = OLD_TO_NEW[parts[0]]
                file_changed = True

            # 2) mantém apenas as linhas com class_id permitido (0)
            if parts[0] in KEEP:
                new_lines.append(" ".join(parts) + "\n")
            else:
                file_removed += 1

        if file_removed > 0:
            removed_lines += file_removed
            file_changed = True

        if file_changed:
            with open(txt, "w") as f:
                f.writelines(new_lines)
            changed_files += 1

print(f"Arquivos processados: {total_files}")
print(f"Arquivos alterados:   {changed_files}")
print(f"Linhas removidas:     {removed_lines}")

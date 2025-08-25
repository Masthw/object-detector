import os

label_dir = "labels/train"  # ajuste se o caminho for diferente
old_class = "570"
new_class = "0"

for file_name in os.listdir(label_dir):
    if not file_name.endswith(".txt"):
        continue

    file_path = os.path.join(label_dir, file_name)

    with open(file_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if parts:
            if parts[0] == old_class:
                parts[0] = new_class
            new_lines.append(" ".join(parts))

    with open(file_path, "w") as f:
        f.write("\n".join(new_lines))

    print(f"✔️ Atualizado: {file_name}")

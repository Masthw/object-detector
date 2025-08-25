import os

labels_dir = "labels/train"
car_ids = set()

for fname in os.listdir(labels_dir):
    if not fname.endswith(".txt"):
        continue
    with open(os.path.join(labels_dir, fname), "r") as f:
        for line in f:
            class_id = line.split()[0]
            car_ids.add(class_id)

print(sorted(car_ids))

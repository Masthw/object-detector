import pandas as pd
import os

# CSV do train (exemplo)
df = pd.read_csv("csv/oidv6-train-annotations-bbox.csv")

# Pega classes
classes = pd.read_csv("class-descriptions-boxable.csv", header=None)
class_dict = {row[0]: idx for idx, row in classes.iterrows()}  # LabelName -> class_id

output_dir = "labels/train"
os.makedirs(output_dir, exist_ok=True)

for image_id, group in df.groupby("ImageID"):
    with open(os.path.join(output_dir, f"{image_id}.txt"), "w") as f:
        for _, row in group.iterrows():
            cls = class_dict[row.LabelName]
            x_center = (row.XMin + row.XMax) / 2
            y_center = (row.YMin + row.YMax) / 2
            w = row.XMax - row.XMin
            h = row.YMax - row.YMin
            f.write(f"{cls} {x_center} {y_center} {w} {h}\n")

import pandas as pd
import os

csv_file = "csv/oidv6-train-annotations-bbox.csv"
classes_file = "csv/class-descriptions-boxable.csv"
images_folder = "./images/train"  # ou validation/test
output_dir = "labels/train"
os.makedirs(output_dir, exist_ok=True)

classes = pd.read_csv(classes_file, header=None)
class_dict = {row[0]: idx for idx, row in classes.iterrows()}


image_ids = set([f.split('.')[0] for f in os.listdir(images_folder)])

chunksize = 100000
for chunk in pd.read_csv(csv_file, chunksize=chunksize):
    chunk = chunk[chunk["ImageID"].isin(image_ids)]
    for image_id, group in chunk.groupby("ImageID"):
        with open(os.path.join(output_dir, f"{image_id}.txt"), "w") as f:
            for _, row in group.iterrows():
                cls = class_dict[row.LabelName]
                xc = (row.XMin + row.XMax) / 2
                yc = (row.YMin + row.YMax) / 2
                w = row.XMax - row.XMin
                h = row.YMax - row.YMin
                f.write(f"{cls} {xc} {yc} {w} {h}\n")

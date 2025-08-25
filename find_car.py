import pandas as pd

# CSV que descreve todas as classes
classes = pd.read_csv("csv/class-descriptions-boxable.csv", header=None, names=["LabelName","ClassName"])

# Imprime todas as classes
for idx, row in classes.iterrows():
    print(f"{idx}: {row.LabelName} -> {row.ClassName}")

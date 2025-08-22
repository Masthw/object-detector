import os

CAR_ID = '/m/0k4j'
splits = ['train', 'validation', 'test']
filenames = ['oidv6-train-annotations-bbox.csv',
             'validation-annotations-bbox.csv',
             'test-annotations-bbox.csv']

with open('car_image_list.txt', 'w') as out_f:
    for split, fname in zip(splits, filenames):
        with open(fname, 'r') as f:
            next(f)  # pula o cabeçalho
            for line in f:
                parts = line.split(',')
                image_id, _, class_id = parts[0], parts[1], parts[2]
                if class_id == CAR_ID:
                    out_f.write(f'{split}/{image_id}\n')

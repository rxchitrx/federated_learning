import os
import torch
from torch.utils.data import random_split

import medmnist
from medmnist import INFO

def prepare_data(num_hospitals=3):
    data_flag = 'pneumoniamnist'
    info = INFO[data_flag]
    DataClass = getattr(medmnist, info['python_class'])

    print("Downloading dataset..")
    full_dataset = DataClass(split='train', download=True)

    total_size = len(full_dataset)
    split_size = total_size // num_hospitals

    lenghts = [split_size] * (num_hospitals - 1)
    lenghts.append(total_size - sum(lenghts))

    hospitals_data = random_split(full_dataset, lenghts)

    if not os.path.exists('data'):
        os.makedirs('data')

    for i, data in enumerate(hospitals_data):
        torch.save(data, f'data/hospital_{i+1}.pt')
        print(f"Hospital {i+1} silo created with {len(data)} images.")

if __name__ == "__main__":
    prepare_data()

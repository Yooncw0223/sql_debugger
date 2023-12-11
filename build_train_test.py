# DIN-SQL.csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import jsonlines
from sklearn.model_selection import train_test_split

from approach1 import Approach1
from approach2 import Approach2
from approach3 import Approach3

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    train_data, test_data = train_test_split(all_data, test_size=0.3, random_state=0)

    approaches = [Approach1, Approach2, Approach3]

    for approach in approaches:
        train_dataset = approach.build_train_dataset(train_data)
        with jsonlines.open(f'{approach.__name__}_train_dataset.jsonl', mode='w') as writer:
            writer.write_all(train_dataset)

    for approach in approaches:
        test_dataset = approach.build_test_dataset(test_data)
        with jsonlines.open(f'{approach.__name__}_test_dataset.jsonl', mode='w') as writer:
            writer.write_all(test_dataset)


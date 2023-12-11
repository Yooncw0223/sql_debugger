import csv
import jsonlines
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    train_data, _ = train_test_split(all_data, test_size=0.3, random_state=0)

    train_dataset_filename = "Approach3_train_dataset.jsonl"

    cur_train = list(jsonlines.open(train_dataset_filename))
    print(cur_train)

    idx = 0
    prompt, predicted, gold, database = train_data[idx]
    print(prompt)

    while len(cur_train) <= idx:
        cur_train.append({"messages": []})

    print(cur_train[idx])

    with jsonlines.open(train_dataset_filename, mode="w") as writer:
        writer.write_all(cur_train)
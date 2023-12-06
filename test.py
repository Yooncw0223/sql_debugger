import build_train_test
import csv

with open('DIN-SQL.csv') as f:
    all_data = list(csv.reader(f))[1:]

idx = 500
prompt, predicted, gold, database = all_data[idx]

print(build_train_test.Approach3.get_system_content())
print()

print(build_train_test.Approach3.get_user_content(prompt, predicted))
print()

print(gold)
print()
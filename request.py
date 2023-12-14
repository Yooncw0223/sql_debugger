import csv

from data_processing.approach3 import Approach3
from evaluate import check_equivalence

index = 500
with open('datasets/DIN-SQL.csv') as f:
    all_data = list(csv.reader(f))[1:]
prompt, predicted, gold, db = all_data[index]

total = 0
count = 0
for prompt, predicted, gold, db in all_data:
    result = check_equivalence(predicted, gold, db)
    if result:
        count += 1

# print(result)
# if count >= LIMIT:
#     break
    total += 1

print("test accuracy", count / total)







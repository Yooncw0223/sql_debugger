import csv

from approach3 import Approach3

index = 500
with open('DIN-SQL.csv') as f:
    all_data = list(csv.reader(f))[1:]
prompt, predicted, gold, db = all_data[index]

print(Approach3.conversation(prompt, predicted, db))





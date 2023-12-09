import evaluate
import csv

with open('DIN-SQL.csv') as f:
    all_data = list(csv.reader(f))[1:]

idx = 500
prompt, predicted, gold, database = all_data[idx]

res = evaluate.evaluate_query(predicted, database)
print(type(res))
print(str(res))
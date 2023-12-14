import evaluate
import csv
import jsonlines

from gpt_interface import get_gpt_response, get_gpt_response_no_json
from evaluate import check_equivalence


reader = jsonlines.open("datasets/Approach1_test_dataset.jsonl")


total = 0
count = 0
for line in reader:
    predicted = get_gpt_response_no_json(line["messages"], model_name="gpt-3.5-turbo-1106")["sql_query"]
    result = check_equivalence(predicted, line["gold"], line["database"])
    if result:
        count += 1

    # print(result)
    # if count >= LIMIT:
    #     break
    total += 1

print("test accuracy", count / total)



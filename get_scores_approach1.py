import jsonlines
import argparse

from approach1 import Approach1
from gpt_interface import get_gpt_response
from evaluate import check_equivalence

parser = argparse.ArgumentParser("get_scores_approach1")
parser.add_argument("-model_name", help="name of model to score on", type=str)
args = parser.parse_args()

filename = f"Approach1_test_dataset.jsonl"
reader = jsonlines.open(filename)
correct = 0
total = 0
for line in reader:
    predicted = get_gpt_response(line["messages"], model_name=args.model_name)["sql_query"]
    if check_equivalence(predicted, line["gold"], line["database"]):
        correct += 1
    total += 1

print(correct / total)
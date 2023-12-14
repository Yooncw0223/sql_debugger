import jsonlines
import argparse
import subprocess

from gpt_interface import get_gpt_response, get_gpt_response_no_json
from evaluate import check_equivalence

parser = argparse.ArgumentParser("get_scores_approach1")
parser.add_argument("--model_name", help="name of model to score on", type=str)
args = parser.parse_args()

filename = "datasets/Approach1_test_dataset.jsonl"

goldFile = "approach1_ft_gold.txt"
predictedFile = "approach1_ft_pred.txt"
reader = jsonlines.open(filename)
correct = 0
total = 0

predicted_list = []
gold_list = []
for line in reader:
    predicted = get_gpt_response_no_json(line["messages"], model_name="ft:gpt-3.5-turbo-0613:personal::8Uthw094")["sql_query"]
    if check_equivalence(predicted, line["gold"], line["database"]):
        correct += 1

    predicted_list.append(predicted)
    gold_list.append(line["gold"])
    total += 1

print("overall db query accuracy", correct / total)

with open(goldFile, "w") as f:
    f.write("\n".join(gold_list))

with open(predictedFile, "w") as f:
    f.write("\n".join(predicted_list))


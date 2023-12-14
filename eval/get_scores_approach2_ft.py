import jsonlines
import argparse
from datetime import datetime

from gpt_interface import get_gpt_response, get_gpt_response_no_json
from evaluate import check_equivalence

parser = argparse.ArgumentParser("get_scores_approach2")
parser.add_argument("--model_name", help="name of model to score on", type=str)
args = parser.parse_args()

filename = "datasets/Approach2_test_dataset.jsonl"
goldFile = "approach2_gold_ft.txt"
predictedFile = "approach2_pred_ft.txt"
reader = jsonlines.open(filename)
correct = 0
total = 0


start = datetime.now()
print("start time", start)

predicted_list = []
gold_list = []
for line in reader:
    predicted = get_gpt_response_no_json(line["messages"], model_name="ft:gpt-3.5-turbo-0613:personal::8Utl2Ucc")["sql_query"]
    if check_equivalence(predicted, line["gold"], line["database"]):
        correct += 1

    predicted_list.append(predicted)
    gold_list.append(line["gold"])
    total += 1

end = datetime.now()
print("end time", end)

print("overall db query accuracy", correct / total)
print("time elapsed", (end - start).total_seconds())

with open(goldFile, "w") as f:
    f.write("\n".join(gold_list))

with open(predictedFile, "w") as f:
    f.write("\n".join(predicted_list))


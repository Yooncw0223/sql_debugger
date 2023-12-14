import jsonlines
import argparse

from evaluate import check_equivalence
from data_processing.approach3 import Approach3

parser = argparse.ArgumentParser("get_scores_approach1")
parser.add_argument("--model_name", help="name of model to score on", type=str)
args = parser.parse_args()

filename = "datasets/Approach3_test_dataset.jsonl"
reader = jsonlines.open(filename)
correct = 0
total = 0

goldFile= "approach3_gold.txt"
predictedFile = "approach3_pred.txt"

predicted_list = []
gold_list = []

correct_when_asking = 0
num_asked = 0
correct_when_not_asking = 0
num_not_asked = 0

for line in reader:
    predicted, entered = Approach3.conversation(line["prompt"], line["predicted"], line["database"])
    if entered:
        if check_equivalence(predicted, line["gold"], line["database"]):
            correct_when_asking += 1
        num_asked += 1
    else:
        if check_equivalence(predicted, line["gold"], line["database"]):
            correct_when_not_asking += 1
        num_not_asked += 1

    # predicted_list.append(predicted)
    # gold_list.append(line["gold"])
    #


print("overall db query accuracy", (correct_when_asking + correct_when_not_asking) / (num_asked + num_not_asked))

print("accuracy when asking", correct_when_asking / num_asked)
print("accuracy when not asking", correct_when_not_asking / num_not_asked)

print("num asked", num_asked)
print("num not asked", num_not_asked)
print("num correct when asked", correct_when_asking)
print("num correct when not asked", correct_when_not_asking)

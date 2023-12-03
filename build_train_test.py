# csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import json
import jsonlines
from sklearn.model_selection import train_test_split

from evaluate import check_equivalence

def build_train_dataset(train_data):
    output_dataset = []
    for line in train_data:
        is_equivalent = check_equivalence(line[1], line[2], line[3])
        if is_equivalent:
            correct_output = json.dumps({"sql_query": line[2], "correct": "true"})
        else:
            correct_output = json.dumps({"sql_query": line[2], "correct": "false"})
        output_dataset.append({'messages':[
            {
                "role": "system", 
                "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."},
            {
                'role': 'user', 
                'content': "How do I express \'" + str(line[0]) + "\' in SQLite? I currently have \'" + str(line[1]) + "\', and if this is correct, please return this query in the format specified below. \
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The correct SQL query\",\
\"correct\": \"Whether the given SQL query is correct\",\
}\
"},
            {
                'role': 'assistant',
                'content': correct_output
            }
],
})
    return output_dataset

def build_test_dataset(test_data):
    output_dataset = []
    for line in test_data:
        output_dataset.append({'messages':[
            {
                "role": "system", 
                "content": "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."},
            {
                'role': 'user', 
                'content': "How do I express \'" + str(line[0]) + "\' in SQLite? I currently have \'" + str(line[1]) + "\', and if this is correct, please return this query in the format specified below.\
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The correct SQL query\",\
\"explanation\": \"How you corrected the query\",\
\"correct\": \"true/false: Is the given SQL query correct\",\
}\
"}
],
                              'gold': line[2],
                              'database': line[3],
})
    return output_dataset

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    num_data = len(all_data)
    train_data, test_data = train_test_split(all_data, test_size=0.3, random_state=0)
    train_dataset = build_train_dataset(train_data)
    test_dataset = build_test_dataset(test_data)
    with jsonlines.open('train_dataset.jsonl', mode='w') as writer:
        writer.write_all(train_dataset)
    with jsonlines.open('test_dataset.jsonl', mode='w') as writer:
        writer.write_all(test_dataset)

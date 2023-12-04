# csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import json
import jsonlines
from sklearn.model_selection import train_test_split

from evaluate import check_equivalence, evaluate_query

class Approach1:
    # Input is prompt
    # Output is SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, given an English prompt."

    @staticmethod
    def get_user_content(prompt):
        return "How do I express \'" + str(prompt) + "\' in SQLite? \
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The SQL query\",\
}\
"

    @staticmethod
    def get_assistant_content(gold):
        correct_output = json.dumps({"sql_query": gold})
        return correct_output

    @classmethod
    def build_train_dataset(cls, train_data):
        output_dataset = []
        for line in train_data:
            prompt, predicted, gold, database, = line
            output_dataset.append({'messages':[
                {
                    "role": "system", 
                    "content": cls.get_system_content()},
                {
                    'role': 'user', 
                    'content': cls.get_user_content(prompt)},
                {
                    'role': 'assistant',
                    'content': cls.get_assistant_content(gold)
                }
    ],
    })
        return output_dataset

    @classmethod
    def build_test_dataset(cls, test_data):
        output_dataset = []
        for line in test_data:
            prompt, predicted, gold, database, = line
            output_dataset.append({'messages':[
                {
                    "role": "system", 
                    "content": cls.get_system_content()},
                {
                    'role': 'user', 
                    'content': cls.get_user_content(prompt)}
                ],
                'gold': gold,
                'database': database,
            })
        return output_dataset

class Approach2:
    # Input is prompt and SQL query
    # Output is corrected SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."

    @staticmethod
    def get_user_content(prompt, predicted):
        return "How do I express \'" + str(prompt) + "\' in SQLite? I currently have \'" + str(predicted) + "\', and if this is correct, please return this query in the format specified below. \
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The correct SQL query\",\
\"correct\": \"Whether the given SQL query is correct\",\
}\
"

    @staticmethod
    def get_assistant_content(predicted, gold, database):
        is_equivalent = check_equivalence(predicted, gold, database)
        if is_equivalent:
            correct_output = json.dumps({"sql_query": gold, "correct": "true"})
        else:
            correct_output = json.dumps({"sql_query": gold, "correct": "false"})
        return correct_output

    @classmethod
    def build_train_dataset(cls, train_data):
        output_dataset = []
        for line in train_data:
            prompt, predicted, gold, database, = line
            output_dataset.append({'messages':[
                {
                    "role": "system", 
                    "content": cls.get_system_content()},
                {
                    'role': 'user', 
                    'content': cls.get_user_content(prompt, predicted)},
                {
                    'role': 'assistant',
                    'content': cls.get_assistant_content(predicted, gold, database)
                }
    ],
    })
        return output_dataset

    @classmethod
    def build_test_dataset(cls, test_data):
        output_dataset = []
        for line in test_data:
            prompt, predicted, gold, database, = line
            output_dataset.append({'messages':[
                {
                    "role": "system", 
                    "content": cls.get_system_content()},
                {
                    'role': 'user', 
                    'content': cls.get_user_content(prompt, predicted)}
                ],
                'gold': gold,
                'database': database,
            })
        return output_dataset

class Approach3:
    # Input is prompt and SQL query and SQL output
    # Output is corrected SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, given an English prompt, a sample SQL query, and that query's output. The given query may already be correct."

    @staticmethod
    def get_user_content(prompt, predicted, predicted_res):
        return "How do I express \'" + str(prompt) + "\' in SQLite? I currently have \'" + str(predicted) + "\', which outputs " +  str(predicted_res) + ". If this is correct, please return this query in the format specified below. \
Create a valid JSON that represents the corrected query:\
{\
\"sql_query\": \"The correct SQL query\",\
\"correct\": \"Whether the given SQL query is correct\",\
}\
"

    @staticmethod
    def get_assistant_content(gold, is_equivalent):
        if is_equivalent:
            correct_output = json.dumps({"sql_query": gold, "correct": "true"})
        else:
            correct_output = json.dumps({"sql_query": gold, "correct": "false"})
        return correct_output

    @classmethod
    def build_train_dataset(cls, train_data):
        output_dataset = []
        for line in train_data:
            prompt, predicted, gold, database, = line

            # if predicted is correct, then prompt, predicted -> gold, true
            # if predicted is wrong, then   prompt, predicted -> gold, false
            #                               gold, predicted   -> gold, true

            is_equivalent, predicted_res, gold_res = check_equivalence(predicted, gold, database, return_sql_outputs=True)
            if is_equivalent:
                output_dataset.append({'messages':[
                    {
                        "role": "system", 
                        "content": cls.get_system_content()},
                    {
                        'role': 'user', 
                        'content': cls.get_user_content(prompt, predicted, predicted_res)},
                    {
                        'role': 'assistant',
                        'content': cls.get_assistant_content(gold, True)
                    }]})
            else:
                output_dataset.append({'messages':[
                    {
                        "role": "system", 
                        "content": cls.get_system_content()},
                    {
                        'role': 'user', 
                        'content': cls.get_user_content(prompt, predicted, predicted_res)},
                    {
                        'role': 'assistant',
                        'content': cls.get_assistant_content(gold, False)
                    }]})
                output_dataset.append({'messages':[
                    {
                        "role": "system", 
                        "content": cls.get_system_content()},
                    {
                        'role': 'user', 
                        'content': cls.get_user_content(prompt, gold, gold_res)},
                    {
                        'role': 'assistant',
                        'content': cls.get_assistant_content(gold, True)
                    }]})
        return output_dataset

    @classmethod
    def build_test_dataset(cls, test_data):
        output_dataset = []
        for line in test_data:
            prompt, predicted, gold, database, = line
            predicted_res = evaluate_query(predicted, database)
            output_dataset.append({'messages':[
                {
                    "role": "system", 
                    "content": cls.get_system_content()},
                {
                    'role': 'user', 
                    'content': cls.get_user_content(prompt, predicted, predicted_res)}
                ],
                'gold': gold,
                'database': database,
            })
        return output_dataset

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    num_data = len(all_data)
    train_data, test_data = train_test_split(all_data, test_size=0.3, random_state=0)

    approaches = [Approach1, Approach2, Approach3]

    train_dataset = []
    for approach in approaches:
        train_dataset += approach.build_train_dataset(train_data)
    with jsonlines.open('train_dataset.jsonl', mode='w') as writer:
        writer.write_all(train_dataset)

    for approach in approaches:
        test_dataset = approach.build_test_dataset(test_data)
        with jsonlines.open(f'{approach.__name__}_test_dataset.jsonl', mode='w') as writer:
            writer.write_all(test_dataset)

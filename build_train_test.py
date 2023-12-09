# csv comes from paper: https://arxiv.org/abs/2304.11015

import csv
import json
import jsonlines
from sklearn.model_selection import train_test_split

import os
from openai import OpenAI
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
        return "You are helping the user debug their SQL query by returning a JSON, \
given an English prompt, and a sample SQL query. \
The given query may already be correct. \
You may ask the user to run a SQL query for you to learn more about the database. \
"

    @staticmethod
    def get_user_content_initial(prompt, predicted):
        return "How do I express \'" + str(prompt) + "\' in SQLite? \
I currently have \'" + str(predicted) + "\'. \
If you'd like, I can also run any SQL query against the database for you. \
Create a valid JSON: \
{\
\"sql_query\": \"The correct SQL query\", \
\"sql_query_to_run\": \"A SQL query for the user to run. Leave as empty string if no extra information about database is needed.\"\
}\
"

    @staticmethod
    def get_user_content_runSQL(sql_query_to_run, database):
        return evaluate_query(sql_query_to_run, database)

    @staticmethod
    def wrap_around_db_result(cls, query_result):
        # should be in {"role": "...", "content": "Here is what we got: {query_result}. Now answer {original question} or ask us to run the query again"} format
        pass

    @classmethod
    def conversation(cls, prompt, predicted, database):
        def get_gpt_response(messages) -> dict:
            # dummy function. eventually, link this up to gpt, and delete this.
            client = OpenAI(api_key=os.environ.get("openaiAPI"))

            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages = [{"role": "system", "content": cls.get_system_content()}, {"role": "user", "content": prompt}],
            )
            result = response.choices[0].message.content
            return json.loads(result if result else "{}")
        response = get_gpt_response([
            {"role": "system", "content": cls.get_system_content()},
            {"role": "user", "content": cls.get_user_content_initial(prompt, predicted)},
        ])
        while response["sql_query_to_run"]:
            response = get_gpt_response([
                {"role": "system", "content": cls.get_system_content()},
                {"role": "user", "content": cls.get_user_content_runSQL(response["sql_query_to_run"], database)},
            ])
        return response["sql_query"]

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    num_data = len(all_data)
    train_data, test_data = train_test_split(all_data, test_size=0.3, random_state=0)

    approaches = [Approach1, Approach2]

    for approach in approaches:
        train_dataset = approach.build_train_dataset(train_data)
        with jsonlines.open(f'{approach.__name__}_train_dataset.jsonl', mode='w') as writer:
            writer.write_all(train_dataset)

    for approach in approaches:
        test_dataset = approach.build_test_dataset(test_data)
        with jsonlines.open(f'{approach.__name__}_test_dataset.jsonl', mode='w') as writer:
            writer.write_all(test_dataset)

SELECT COUNT(*) FROM singer,SELECT count(*) FROM singer,concert_singer
Approach3.conversation("How many singers do we have?", )

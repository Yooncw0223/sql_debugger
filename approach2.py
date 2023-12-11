import json

from evaluate import check_equivalence

class Approach2:
    # Input is prompt and SQL query
    # Output is corrected SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, given an English prompt and a sample SQL query. The given query may already be correct."

    @staticmethod
    def get_user_content(prompt, predicted):
        return "How do I express \'" + str(prompt) + "\' in SQLite? I currently have \'" + str(predicted) + "\', and if this is correct, please return this query in the format specified below. \
Only give me exactly the information that is asked for. Create a valid JSON that represents the corrected query:\
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

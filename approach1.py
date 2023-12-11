import json

class Approach1:
    # Input is prompt
    # Output is SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, given an English prompt."

    @staticmethod
    def get_user_content(prompt):
        return "How do I express \'" + str(prompt) + "\' in SQLite? \
Only give me exactly the information that is asked for. Create a valid JSON that represents the corrected query:\
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
                }]})
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

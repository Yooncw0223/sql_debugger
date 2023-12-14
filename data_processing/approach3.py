from evaluate import evaluate_query
from gpt_interface import get_gpt_response, get_gpt_response_no_json

class Approach3:
    # Input is prompt and SQL query and SQL output
    # Output is corrected SQL query

    @staticmethod
    def get_system_content():
        return "You are helping the user debug their SQL query by returning a JSON, \
given an English prompt, and a sample SQL query. \
The given query may already be correct. \
You may ask the user to run a SQL query for you to learn more about the database."

    @staticmethod
    def get_user_content_initial(prompt: str, predicted: str) -> str:
        return "How do I express \'" + prompt + "\' in SQLite? \
I currently have \'" + predicted + "\'. \
If you'd like, I can also run any SQL query against the database for you. \
Only give me exactly the information that is asked for. Create a valid JSON: \
{\
\"sql_query\": \"The correct SQL query\", \
\"sql_query_to_run\": \"A SQL query for the user to run. Leave as empty string if no extra information about database is needed.\"\
}\
"

    @staticmethod
    def get_user_content_runSQL(sql_query_to_run, database):
        res = evaluate_query(sql_query_to_run, database)
        return str(res)

    @classmethod
    def conversation(cls, prompt, predicted, database, model="gpt-3.5-turbo-1106"):
        messages = []
        messages.append({"role": "system", "content": cls.get_system_content()})
        messages.append({"role": "user", "content": cls.get_user_content_initial(prompt, predicted)})
        response = get_gpt_response(messages, model_name=model)
        entered = False
        try:
            while response["sql_query_to_run"]:
                entered = True
                messages.append({"role": "assistant", "content": str(response)})
                messages.append({"role": "user", "content": cls.get_user_content_runSQL(response["sql_query_to_run"], database)})
                response = get_gpt_response(messages, model_name=model)
            return response["sql_query"], entered 
        except:
            return predicted, entered 

    @classmethod
    def conversation_ft(cls, prompt, predicted, database, model="gpt-3.5-turbo-1106"):
        # fine-tuned model can return incorrect string
        messages = []
        messages.append({"role": "system", "content": cls.get_system_content()})
        messages.append({"role": "user", "content": cls.get_user_content_initial(prompt, predicted)})
        response = get_gpt_response_no_json(messages, model_name=model)
        entered = False
        try:
            while response["sql_query_to_run"]:
                entered = True
                messages.append({"role": "assistant", "content": str(response)})
                messages.append({"role": "user", "content": cls.get_user_content_runSQL(response["sql_query_to_run"], database)})
                response = get_gpt_response_no_json(messages)
            return response["sql_query"], entered 
        except:
            return predicted, entered 

    @classmethod
    def build_train_dataset(cls, train_data):
        # Not yet implemented
        return []

    @classmethod
    def build_test_dataset(cls, test_data):
        output_dataset = []
        for line in test_data:
            prompt, predicted, gold, database, = line
            output_dataset.append({
                'prompt': prompt,
                'predicted': predicted,
                'gold': gold,
                'database': database,
            })
        return output_dataset

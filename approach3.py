from evaluate import evaluate_query
from gpt_interface import get_gpt_response

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
        res = evaluate_query(sql_query_to_run, database)
        return str(res)

    @staticmethod
    def wrap_around_db_result(cls, query_result):
        # should be in {"role": "...", "content": "Here is what we got: {query_result}. Now answer {original question} or ask us to run the query again"} format
        pass

    @classmethod
    def conversation(cls, prompt, predicted, database):
        # def get_gpt_response(messages) -> dict:
        #     # dummy function. eventually, link this up to gpt, and delete this.
        #     client = OpenAI(api_key=os.environ.get("openaiAPI"))
        #
        #     response = client.chat.completions.create(
        #         model="gpt-3.5-turbo-1106",
        #         response_format={ "type": "json_object" },
        #         messages = [{"role": "system", "content": cls.get_system_content()}, {"role": "user", "content": prompt}],
        #     )
        #     result = response.choices[0].message.content
        #     return json.loads(result if result else "{}")
        response = get_gpt_response([
            {"role": "system", "content": cls.get_system_content()},
            {"role": "user", "content": cls.get_user_content_initial(prompt, predicted)},
        ])
        while response["sql_query_to_run"]:
            print("conversation running")
            response = get_gpt_response([
                {"role": "system", "content": cls.get_system_content()},
                {"role": "user", "content": cls.get_user_content_runSQL(response["sql_query_to_run"], database)},
            ])
        return response["sql_query"]

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
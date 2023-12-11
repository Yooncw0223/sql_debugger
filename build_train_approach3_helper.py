import csv
import json
import jsonlines
from sklearn.model_selection import train_test_split

from approach3 import Approach3
from evaluate import check_equivalence, evaluate_query

if __name__ == "__main__":
    with open('DIN-SQL.csv') as f:
        all_data = list(csv.reader(f))[1:]
    train_data, _ = train_test_split(all_data, test_size=0.3, random_state=0)

    train_dataset_filename = "Approach3_train_dataset.jsonl"

    cur_train = list(jsonlines.open(train_dataset_filename))

    idx = 1
    print(f"working on idx {idx}")
    prompt, predicted, gold, database = train_data[idx]

    while len(cur_train) <= idx:
        cur_train.append({"messages": [
            {"role": "system", "content": Approach3.get_system_content()},
            {"role": "user", "content": Approach3.get_user_content_initial(prompt, predicted)}
        ]})

    add_assistant_response = None

    cur_messages = cur_train[idx]["messages"]
    if cur_messages[-1]["role"] != "assistant":
        if add_assistant_response is None:
            print("please add assistant response")
            print()
            for message in cur_messages:
                role, content = message["role"], message["content"]
                print(role)
                print(content)
                print()
        else:
            cur_messages.append({"role": "assistant", "content": json.dumps(add_assistant_response)})
            print("added assistant response. if everything looks correct, set add_assistant_respone=None")
    else:
        if add_assistant_response is not None:
            print("the assistant response already seems to be added. please explicitly set add_assistant_response=None")
            raise Exception
        final_query = json.loads(cur_messages[-1]["content"])["sql_query"]
        is_equivalent, final_query_res, gold_res = check_equivalence(final_query, gold, database, return_sql_outputs=True)
        if is_equivalent:
            print("equivalent")
        else:
            print("not equivalent")
            print(predicted)
            print(final_query)
            print(gold)
            print(prompt)
            print()
            print(final_query_res)
            print(gold_res)

    with jsonlines.open(train_dataset_filename, mode="w") as writer:
        writer.write_all(cur_train)
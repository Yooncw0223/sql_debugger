
import argparse
import gpt_interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', dest='query', type=str, help="query you want to test")
    parser.add_argument('--prompt', dest='prompt', type=str, help="what the query should be doing")

    args = parser.parse_args()

    model = "model"
    # gpt_interface


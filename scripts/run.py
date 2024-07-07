import argparse
import json
import logging

from handler import lambda_handler


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Path to a JSON file to parse.")
    p.add_argument("--log", help="Log level", default=logging.WARNING, choices=logging._nameToLevel.keys())
    return p.parse_args()


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def main():
    args = parse_args()
    logging.getLogger().setLevel(level=logging.getLevelName(args.log))

    body = json.loads(read_file(args.input))
    result = lambda_handler(body, None)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

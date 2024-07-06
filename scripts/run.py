import argparse
import json
import logging

from handler import lambda_handler


def parseArgs():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="Inline JSON OR path to a JSON file, containing shifts and members.")
    p.add_argument("--log", help="Log level", default=logging.WARNING, choices=logging._nameToLevel.keys())
    return p.parse_args()


def read_file(path: str) -> str:
    """Reads a file and returns a string."""
    with open(path, "r") as f:
        return f.read()


def main():
    args = parseArgs()
    logging.getLogger().setLevel(level=logging.getLevelName(args.log))

    body = json.loads(read_file(args.input))
    result = lambda_handler(body, None)

    print(json.dumps(result))


if __name__ == "__main__":
    main()

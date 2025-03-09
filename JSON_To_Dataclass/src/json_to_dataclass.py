import argparse
import json
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from JSON_To_Dataclass.src.DCObject import DCObject

tab = "\t"

parser = argparse.ArgumentParser(
    description="Converts JSON file to Dataclass",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    exit_on_error=True,
    add_help=True,
    prog="JSON_To_Dataclass",
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    help="Direct system path to a JSON file",
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Directory the place output .py file with Dataclass"
)

parser.add_argument(
    "-d",
    "--directory",
    type=str,
    help="Directory to JSON files, will parse all files within into data classes."
)

parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="Name of parent Dataclass",
)

parser.add_argument(
    "-ad",
    "--apply_defaults",
    type=bool,
    help="Apply default values for all fields using the values within provided JSON file",
)

def get_default_path(is_input=False):
    cwd = os.getcwd()
    os.listdir(cwd)

    json_files = []
    for file in os.listdir(cwd):
        if file.endswith(".json"):
            json_files.append(os.path.join(cwd, file))

    if json_files and len(json_files) == 1:
        return os.path.join(json_files[0])
    elif json_files and is_input:
        return None
    elif json_files and len(json_files) > 1:
        return json_files
    else:
        raise Exception("No JSON files found in current directory.  "
                        "Provide directory or JSON files using --directory or --input")



parser.set_defaults(
    input=get_default_path(is_input=True),
    output=os.path.join(os.getcwd(), "sample.py"),
    directory=get_default_path(),
    name="GeneratedDataclass"
)

args = parser.parse_args()

json_data = None

try:
    with open(args.input, "r") as f:
        json_data = json.loads(f.read())
except FileNotFoundError:
    print("Provided input file path does not exist")
    exit(1)
except json.decoder.JSONDecodeError:
    print("Provided input file path does not contain a valid JSON file or file contains malformed JSON")
    exit(1)

name = re.findall(r"\S", args.name)

if isinstance(name, list):
    name = "".join(name)
elif not name:
    print("\nProvided name was empty, defaulting back to GeneratedDataclass")
    name = "GeneratedDataclass"

try:
    dc_builder = DCObject(
        name,
        args.apply_defaults,
        json_data,
        top_parent=True
    )
    if not args.output.endswith(".py"):
        args.output += ".py"
    with open(args.output, "w") as f:
        f.write(dc_builder.build())
        print("File created successfully at {}".format(args.output))
        exit(0)
except FileNotFoundError:
    print("Provided output file path does not exist")
    exit(1)




import argparse
import json
import os
import re

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
)

parser.add_argument(
    "-o",
    "--output",
    type=str,
)

parser.add_argument(
    "-d",
    "--directory",
    type=str,
)

parser.add_argument(
    "-n",
    "--name",
    type=str,
)

parser.add_argument(
    "-ad",
    "--apply_defaults",
    type=bool,
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

def handle_defaults(value, default):
    return f"={value}" if default else ''

def handle_lists(key, value, default):
    types = []
    inside_classes = []
    dataclass_output = ''
    for item in value:
        if type(item) == dict:
            inner_dc = create_dataclass(item, key, default)
            if inner_dc not in inside_classes:
                inside_classes.append(inner_dc)
                types.append(key[0].upper() + key[1:])



            # for inner_key in item.keys():
            #     if inner_key not in types:
            #         types.append(inner_key[0].upper() + inner_key[1:])

        elif type(item) == list:
            inner_dt_output, inner_classes = handle_lists(key, item, default)
            dataclass_output += inner_dt_output
            inside_classes += inner_classes
        else:
            evaluate_type = re.findall(r"'([^']*)'", str(type(item)))[0]
            if evaluate_type not in types:
                    types.append(evaluate_type)

    dataclass_output += f"{tab}{key}: list[{' | '.join(types)}]\n"
    return dataclass_output, inside_classes

def create_dataclass(data, dataclass_name, make_values_default=False):

    inside_classes = []
    dataclass_output = f"class {dataclass_name[0].upper() + dataclass_name[1:]}:\n"
    if isinstance(data, dict):
        for key, value in data.items():
            if type(value) == dict:
                dataclass_output += f"{tab}{key}: {key[0].upper() + key[1:]}\n"
                inside_classes.append(create_dataclass(value, key, make_values_default))
            elif type(value) == list:
                dc_list_output, inner_classes = handle_lists(key, value, make_values_default)
                dataclass_output += dc_list_output
                inside_classes += inner_classes
            else:
                evaluate_type = re.findall(r"'([^']*)'", str(type(value)))[0]
                dataclass_output += f"{tab}{key}: {evaluate_type}{handle_defaults(value, make_values_default)}\n"

        init_output = ''
        if inside_classes and len(inside_classes) > 0:
            init_output = '\n\n'.join(inside_classes)
        return f"{init_output}\n\n{dataclass_output}"
    elif isinstance(data, list):
        init_output = ''
        dataclass_output, inside_classes = handle_lists(dataclass_name, data, make_values_default)
        if inside_classes and len(inside_classes) > 0:
            init_output = '\n\n'.join(inside_classes)
        return f"{init_output}"

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
    final_output = create_dataclass(json_data, name, make_values_default=args.apply_defaults)
    if not args.output.endswith(".py"):
        args.output += ".py"
    with open(args.output, "w") as f:
        f.write(final_output)
        print("File created successfully at {}".format(args.output))
        exit(0)
except FileNotFoundError:
    print("Provided output file path does not exist")
    exit(1)




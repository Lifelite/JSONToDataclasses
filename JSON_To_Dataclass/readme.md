# JSON to Dataclass

Just a simple tool that creates dataclasses from JSON files by assessing the JSON schema structure and 
building typed dataclasses into a .py file

### Requirements
_______
>Python 3.12

### Installation
______

`pip install json_to_dataclass`

### Command Syntax
_____

cd {DIRECTORY}
`$ python json_to_dataclass.py -h`

```optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Direct system path to a JSON file (default: ${CWD}/sample.json)
  -o OUTPUT, --output OUTPUT
                        Directory the place output .py file with Dataclass (default: ${CWD}/sample.py)
  -d DIRECTORY, --directory DIRECTORY
                        Directory to JSON files, will parse all files within into data classes. (default: ${CWD}/sample.json)
  -n NAME, --name NAME  Name of parent Dataclass (default: GeneratedDataclass)
  -ad APPLY_DEFAULTS, --apply_defaults APPLY_DEFAULTS
                        Apply default values for all fields using the values within provided JSON file (default: None)
```
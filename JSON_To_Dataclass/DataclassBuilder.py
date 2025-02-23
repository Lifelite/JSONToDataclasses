import re

tab = "\t"

class DataclassBuilder:
    def __init__(self, name:str, data:dict | list, default:bool=False):
        self.default = default
        self.name = name
        self.inside_classes = []
        self.data = data

    def _handle_defaults(self, value):
        return f"={value}" if self.default else ''

    def handle_lists(self, key, value):
        types = []
        for item in value:
            if type(item) == dict:
                inner_dc = self.create_dataclass(value, key, inner=True)
                if inner_dc not in self.inside_classes:
                    self.inside_classes.append(inner_dc)
                    types.append(key[0].upper() + key[1:])
            elif type(item) == list:
                types.appent(self.handle_lists(key, item))
            else:
                evaluate_type = re.findall(r"'([^']*)'", str(type(item)))[0]
                if evaluate_type not in types:
                    types.append(evaluate_type)

        return f"{tab}{key}: list[{' | '.join(types)}]\n"

    def handle_dict(self, data):
        dataclass_output = ""
        for key, value in data.items():

            if type(value) == dict:
                dataclass_output += f"{tab}{key}: {key[0].upper() + key[1:]}\n"
                self.inside_classes.append(self.create_dataclass(value, key, inner=True))
            elif type(value) == list:
                dataclass_output += self.handle_lists(key, value)
            else:
                evaluate_type = re.findall(r"'([^']*)'", str(type(value)))[0]
                dataclass_output += f"{tab}{key}: {evaluate_type}{self._handle_defaults(value)}\n"

        return dataclass_output

    def create_dataclass(self, data=None, dataclass_name=None, inner=False):
        if data is None:
            data =self.data
        if dataclass_name is None:
            dataclass_name = self.name

        dataclass_output = f"class {dataclass_name[0].upper() + dataclass_name[1:]}:\n"

        if isinstance(data, dict):
            dataclass_output += self.handle_dict(data)

        elif isinstance(data, list):
            init_output = ''
            self.handle_lists(dataclass_name, data)
            return f"{init_output}"

        init_output = ''
        if inner:
            return f"{dataclass_output}"
        if self.inside_classes and len(self.inside_classes) > 0:
            init_output = '\n'.join(self.inside_classes)
        return f"{init_output}\n\n{dataclass_output}"
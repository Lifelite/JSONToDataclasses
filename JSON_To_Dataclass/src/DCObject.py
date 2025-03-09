import dataclasses
from typing import Any

counter = 0


class DCObject:
    IMPORT_STRING = import_string = "from dataclasses import dataclass\n"
    DECORATION_STRING = "@dataclass\nclass"
    file_name = None

    def __init__(
            self,
            class_name: str = None,
            defaults: bool = None,
            *args,
            **kwargs
    ):
        if class_name is None:
            self.name = "JSONFile"
            self.top_parent = True
        else:
            self.name = class_name[0].upper() + class_name[1:]

        self.inner_classes = []
        self.inner_lists = []
        self.attribute_strings = []
        self.defaults = defaults
        self.top_parent = False
        self.class_declare = f"{self.DECORATION_STRING} {self.name}:\n"
        if kwargs.get("top_parent"):
            self.top_parent = True
        elif kwargs:
            self.handle_kwargs(**kwargs)
        if args:
            self.handle_args(*args)

    @staticmethod
    def parse_type(value: Any) -> Any:
        value_type = type(value)
        return value_type.__name__ if value_type else value_type

    def handle_args(self, *args: list):
        if self.top_parent and len(args) == 1:
            inner_item = args[0]
            if isinstance(inner_item, dict):
                self.handle_kwargs(**inner_item)
                return
            elif isinstance(inner_item, list):
                args = args[0]

        global counter
        for inner_obj in args:

            if isinstance(inner_obj, dict):
                try:
                    inner_dc = DCObject(
                        **inner_obj,
                        defaults=self.defaults,
                        class_name="DictObject",
                    )
                except TypeError:

                    value = inner_obj.pop("class_name", None)
                    value = inner_obj.pop("defaults", value)
                    value = inner_obj.pop("top_parent", value)

                    inner_obj["arg_conflict_object"] = value
                    inner_dc = DCObject(
                        self.defaults,
                        **inner_obj,
                        class_name="DictObject",
                    )

                self.inner_classes.append(inner_dc)
                inner_name = inner_dc.name
                inner_name = inner_name[0].lower() + inner_name[1:]
                self.attribute_strings.append(
                    f"\t{inner_name}_list: "
                    f"list[{inner_dc.name}]"
                )
                break
            # IN case of multidimensional lists.
            elif isinstance(inner_obj, list):
                inner_class = DCObject(self.name, self.defaults, inner_obj)
                if inner_class.inner_classes:
                    self.inner_classes += inner_class.inner_classes
                    self.attribute_strings.append(f"\t{self.name}: {inner_class.name}")
                if inner_class.inner_lists:
                    self.inner_lists += inner_class.inner_lists
                    self.attribute_strings.append(
                        f"\t{self.name}: {self.strip_attributes(inner_class.attribute_strings)}"
                    )
            else:
                self.inner_lists.append(self.parse_type(inner_obj))
                counter += 1

    @staticmethod
    def strip_attributes(string_list: [str]):
        parsed_strings = []
        for string in string_list:
            if string.startswith("\t"):
                string = string[1:]
            index = string.find(":")
            if index != -1:
                parsed_strings.append(string[:index])
            else:
                parsed_strings.append(string)
        return parsed_strings

    def handle_kwargs(self, **kwargs):
        for key, inner_obj in kwargs.items():
            if isinstance(inner_obj, dict):
                inner_class = DCObject(key, self.defaults, **inner_obj)
                self.inner_classes.append(inner_class)
                self.attribute_strings.append(f"\t{key}: {inner_class.name}")
            elif isinstance(inner_obj, list):
                inner_class = DCObject(key, self.defaults, *inner_obj)
                if inner_class.inner_classes:
                    self.inner_classes.append(inner_class.inner_classes)
                    self.attribute_strings.append(f"\t{key}: {inner_class.name}")
                if inner_class.inner_lists:
                    self.inner_lists += inner_class.inner_lists
                    inner_types = []
                    if not inner_class.attribute_strings and inner_class.inner_lists:
                        for item in inner_class.inner_lists:
                            if item not in inner_types:
                                inner_types.append(item)
                        stripped_strings = inner_types
                    else:
                        stripped_strings = self.strip_attributes(inner_class.attribute_strings)

                    type_list = f"list[{', '.join(stripped_strings)}]"

                    self.attribute_strings.append(
                        f"\t{key}: {type_list}"
                    )
            else:

                self.attribute_strings.append(f"\t{key}: {self.parse_type(inner_obj)}")

    def build(self):
        file_string = ''
        if self.top_parent:
            file_string += self.IMPORT_STRING
        if self.inner_classes:
            for inner_dc in self.inner_classes:
                file_string += inner_dc.build()
        file_string += "\n\n"
        file_string += self.class_declare
        file_string += "\n".join(self.attribute_strings)
        return file_string

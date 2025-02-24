from dataclasses import dataclass

@dataclass
class DeviceType:
	type: str

@dataclass
class Properties:
	deviceType: DeviceType

@dataclass
class DeviceType:
	const: str

@dataclass
class OneOf:
	properties: Properties
	$ref: str


@dataclass
class GeneratedDataclass:
	$id: str
	$schema: str
	type: str
	properties: Properties
	required: list[str]
	oneOf: list[OneOf]



class GlossDef:
	para: str
	GlossSeeAlso: list[str]


class GlossEntry:
	ID: str
	SortAs: str
	GlossTerm: str
	Acronym: str
	Abbrev: str
	GlossDef: GlossDef
	GlossSee: str


class GlossList:
	GlossEntry: GlossEntry


class GlossDiv:
	title: str
	GlossList: GlossList


class Glossary:
	title: str
	GlossDiv: GlossDiv


class GeneratedDataclass:
	glossary: Glossary

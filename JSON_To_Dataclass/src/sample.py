from dataclasses import dataclass


@dataclass
class Q1:
	question: str
	options: list[str]
	answer: str

@dataclass
class Sport:
	q1: Q1

@dataclass
class Q1:
	question: str
	options: list[str]
	answer: str

@dataclass
class Q2:
	question: str
	options: list[str]
	answer: str

@dataclass
class Maths:
	q1: Q1
	q2: Q2

@dataclass
class Quiz:
	sport: Sport
	maths: Maths

@dataclass
class GeneratedDataclass:
	quiz: Quiz
class Q1:
	question: str
	options: list[str]
	answer: str

class Sport:
	q1: Q1

class Q2:
	question: str
	options: list[str]
	answer: str

class Maths:
	q1: Q1
	q2: Q2

class Quiz:
	sport: Sport
	maths: Maths


class GeneratedDataclass:
	quiz: Quiz

from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
	IDENTIFIER	= 0
	LITERAL     = 1
	PLUS        = 2
	MINUS       = 3
	MULTIPLY    = 4
	ASSIGNMENT  = 5
	LPAREN      = 6
	RPAREN      = 7
	DIVIDE      = 8
	ADD					= 9
	SUBTRACT		= 10

@dataclass
class Token:
	type: TokenType
	value: any = None

	def __repr__(self):
		return self.type.name + (f":{self.value}" if self.value != None else "")
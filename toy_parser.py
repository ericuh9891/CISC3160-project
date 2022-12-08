from toy_tokens import TokenType, Token
from toy_nodes import *

# Probably safe to use original CFG since the lexer filters out left recursive grammar

class Parser:
	tokens: list[Token]
	variables: dict[str, int]

	def __init__(self, tokens, variables):
		self.tokens = iter(tokens)
		self.variables = variables
		self.next_token()

	def raise_error(self):
		raise Exception("Invalid token")
	
	def next_token(self):
		try:
			self.current_token = next(self.tokens)
		except StopIteration:
			self.current_token = None

	# Program => Assignment*
	def parse(self):
		if self.current_token == None:
			return None

		result = self.assignment()

		if self.current_token != None:
			self.raise_error()

		return result

	# Assignment -> Identifier = Exp;
	def assignment(self):

		while self.current_token != None and self.current_token.type in (TokenType.IDENTIFIER, TokenType.ASSIGNMENT):
			if self.current_token.type == TokenType.IDENTIFIER:
				result = IdentifierNode(self.current_token.value)
				self.next_token()
			elif self.current_token.type == TokenType.ASSIGNMENT:
				self.next_token()
				result = AssignmentNode(result, self.expression())

		return result

	# Exp -> Exp + Term | Exp - Term | Term
	def expression(self):
		result = self.term()

		while self.current_token != None and self.current_token.type in (TokenType.ADD, TokenType.SUBTRACT):
			if self.current_token.type == TokenType.ADD:
				self.next_token()
				result = AddNode(result, self.term())
			elif self.current_token.type == TokenType.SUBTRACT:
				self.next_token()
				result = SubtractNode(result, self.term())

		return result

	# Term -> Term * Fact | Fact
	def term(self):
		result = self.factor()

		while self.current_token != None and self.current_token.type == TokenType.MULTIPLY:
			if self.current_token.type == TokenType.MULTIPLY:
				self.next_token()
				result = MultiplyNode(result, self.factor())
				
		return result

	# Fact -> (Exp) | -Fact | +Fact | Literal | Identifier
	def factor(self):
		token = self.current_token

		if token.type == TokenType.LPAREN:
			self.next_token()
			result = self.expression()

			if self.current_token.type != TokenType.RPAREN:
				self.raise_error()
				
			self.next_token()
			return result

		elif token.type == TokenType.IDENTIFIER:
			self.next_token()
			
			if bool(self.variables) and self.variables.get(token.value) != None:
				return IdentifierNode(self.variables.get(token.value))
			else:
				raise NameError(f"Variable: '{token.value}' has not been initialized")

		elif token.type == TokenType.LITERAL:
			self.next_token()
			return NumberNode(token.value)

		elif token.type == TokenType.PLUS:
			self.next_token()
			return PlusNode(self.factor())
		
		elif token.type == TokenType.MINUS:
			self.next_token()
			return MinusNode(self.factor())
		
		self.raise_error()
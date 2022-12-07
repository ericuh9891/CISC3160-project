from toy_tokens import TokenType, Token
from toy_nodes import *

class Parser:
	tokens: list[Token]
	# variables: dict[str, int]

	def __init__(self, tokens):
		self.tokens = iter(tokens)
		# self.variables = variables
		self.advance()

	def raise_error(self):
		raise Exception("Invalid token")
	
	def advance(self):
		try:
			self.current_token = next(self.tokens)
		except StopIteration:
			self.current_token = None

	def parse(self):
		if self.current_token == None:
			return None

		result = self.assignment()

		if self.current_token != None:
			self.raise_error()

		return result

	def assignment(self):
		result = self.expression()

		while self.current_token != None and self.current_token.type == TokenType.ASSIGNMENT:
			if self.current_token.type == TokenType.ASSIGNMENT:
				self.advance()
				result = AssignmentNode(result, self.expression())

		return result

	def expression(self):
		result = self.term()

		while self.current_token != None and self.current_token.type in (TokenType.ADD, TokenType.SUBTRACT):
			if self.current_token.type == TokenType.ADD:
				self.advance()
				result = AddNode(result, self.term())
			elif self.current_token.type == TokenType.SUBTRACT:
				self.advance()
				result = SubtractNode(result, self.term())

		return result

	def term(self):
		result = self.factor()

		while self.current_token != None and self.current_token.type == TokenType.MULTIPLY:
			if self.current_token.type == TokenType.MULTIPLY:
				self.advance()
				result = MultiplyNode(result, self.factor())
				
		return result

	def factor(self):
		token = self.current_token

		if token.type == TokenType.LPAREN:
			self.advance()
			result = self.expression()

			if self.current_token.type != TokenType.RPAREN:
				self.raise_error()
			
			self.advance()
			return result

		elif token.type == TokenType.IDENTIFIER:
			self.advance()
			
			# variable = self.variables.get(token.value)
			# print(f"Parser variable replacement: {variable}")
			# if not bool(self.variables) and variable != None:
			# else:
			# 	raise Exception(f"Variable ({token.value}) not defined")
			return IdentifierNode(token.value) # LOOKUP value and replace, if variable doesn't exist then raise error

		elif token.type == TokenType.LITERAL:
			self.advance()
			return NumberNode(token.value)

		elif token.type == TokenType.PLUS:
			self.advance()
			return PlusNode(self.factor())
		
		elif token.type == TokenType.MINUS:
			self.advance()
			return MinusNode(self.factor())
		
		self.raise_error()
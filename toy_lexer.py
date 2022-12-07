from toy_tokens import Token, TokenType

class Lexer():
	ALPHABETS_ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
	DIGITS = "0123456789"
	NON_ZERO_DIGIT = "123456789"

	input_char: str 
	current_index: int
	statement: str
	token_start: int
	tokens: list[Token]
	identifier_flag = False
	literal_flag = False

	def __init__(self, statement):
		# initialize variables
		self.statement = statement
		self.current_index = 0
		self.tokens: list[Token] = []
		# start lexer
		if not self.tokenize():
			raise SyntaxError()

	def __repr__(self):
		return f'Statement: {self.statement} Tokenized into \n{self.tokens}'

	# creates tokens during the recursive descent parsing for syntax checking
	def next_char(self):
		if self.current_index >= len(self.statement):
			self.input_char = '$'
		else:
			self.input_char = self.statement[self.current_index]

			### create tokens ###
			# When a literal begins, First(Literal) = {0,1,2,3,4,5,6,7,8,9}
			if True and self.input_char in Lexer.DIGITS and self.literal_flag == False and self.identifier_flag == False:
				self.literal_flag = True
				self.token_start = self.current_index

			# When a literal ends, Follow(Literal) = {*,+,-,;,)}
			elif self.input_char in '*+-;)' and self.literal_flag == True:
				self.literal_flag = False
				self.tokens.append(Token(TokenType.LITERAL, int(self.statement[self.token_start:self.current_index])))
			
			# When an identifier begins, First(I) = {a,b,c,...,x,y,z,A,B,C,...,X,Y,Z,_}
			elif self.input_char in Lexer.ALPHABETS_ and self.identifier_flag == False:
				self.identifier_flag = True
				self.token_start = self.current_index
			
			# When an identifier ends, Follow(I) = {=,*,+,-,;,)}
			elif self.input_char in '=*+-;)' and self.identifier_flag == True:
				self.identifier_flag = False
				self.tokens.append(Token(TokenType.IDENTIFIER, self.statement[self.token_start:self.current_index]))

			match self.input_char:
				case '=':
					self.tokens.append(Token(TokenType.ASSIGNMENT))

				case '-': 
					if self.tokens[-1].type in (TokenType.LITERAL, TokenType.IDENTIFIER):
						self.tokens.append(Token(TokenType.SUBTRACT))
					else:
						self.tokens.append(Token(TokenType.MINUS))

				case '+': 
					if self.tokens[-1].type in (TokenType.LITERAL, TokenType.IDENTIFIER):
						self.tokens.append(Token(TokenType.ADD))
					else:
						self.tokens.append(Token(TokenType.PLUS))

				case '*':
					self.tokens.append(Token(TokenType.MULTIPLY))

				case '(':
					self.tokens.append(Token(TokenType.LPAREN))

				case ')':
					self.tokens.append(Token(TokenType.RPAREN))

			self.current_index += 1
	
	def match(self, expected_char: str):
		if self.input_char != expected_char:
			return False

		self.next_char()
		return True

	# starts parsing
	def tokenize(self):
		self.next_char()
		# the start production rule
		if not self.assignment():
			return False
		# if it's an assignment then the last char should be a $
		return self.match('$')

	# get list of tokens
	def getTokens(self) -> list[Token]:
		return self.tokens

	# Production rule: A -> I=E;
	def assignment(self):
		if not self.identifier():
			return False

		if not self.match('='):
			return False

		if not self.expression():
			return False

		return self.match(';')

	# Production rule: E -> TE'
	def expression(self):

		if not self.term():
			return False

		if not self.expression_prime():
			return False

		return True

	# Production rule: E' -> +TE' | -TE' | ε
	def expression_prime(self):
		match self.input_char:
			case '+':
				if not self.term():
					return False
				if not self.expression_prime():
					return False
				return True

			case '-':
				if not self.term():
					return False
				if not self.expression_prime():
					return False
				return True

			case ';' | ')':
				return True

			case _:
				return False

	# Production rule: T -> FT'
	def term(self):
		if not self.factor():
			return False

		if not self.term_prime():
			return False

		return True

	# Production rule: T' -> *FT' | ε
	def term_prime(self):
		match self.input_char:
			case '*':
				self.next_char()
				if not self.factor():
					return False
				if not self.term_prime():
					return False
				return True

			# terminating case for recursive call
			case '+' | '-' | ';' | ')':
				return True

			case _:
				return False
	
	# Production rule: F -> (E) | -F | +F | Literal | I
	def factor(self):
		# Literal
		if self.input_char in Lexer.DIGITS:
			return self.literal()

		# I
		if self.input_char in Lexer.ALPHABETS_:
			return self.identifier()

		match self.input_char:
			# (E)
			case '(':
				self.next_char()
				if not self.expression():
					return False
				return self.match(')')

			# -F | +F
			case '+':
				self.next_char()
				if not self.factor():
					return False
				return True

			case '-':
				self.next_char()
				if not self.factor():
					return False
				return True

			# Follow(F) = {*,+,-,;,)} terminating case
			case '*' | '+' | '-' | ';' | ')':
				return True

			case _:
				return False
	
	# Production rule: I -> Letter [Letter|D]*
	def identifier(self):
		if not self.letter():
			return False

		if not self.letter_or_digit():
			return False

		return True

	# Production rule: Letter -> a|b|c|...|x|y|z|A|B|C|...|X|Y|Z|_
	def letter(self):
		if self.input_char in Lexer.ALPHABETS_:
			self.next_char()
			return True

		return False

	# Production rule: Literal -> 0 | NZ D*
	def literal(self):
		if self.input_char == '0':
			self.next_char()
			return True

		if not self.non_zero_digit():
			return False

		if not self.zero_or_more_digit():
			return False

		return True

	# Production rule: NZ -> 1|2|3|...|7|8|9
	def non_zero_digit(self):
		if self.input_char in Lexer.NON_ZERO_DIGIT:
			self.next_char()
			return True

		return False
	
	# Production rule: D -> 0|1|2|...|7|8|9
	def digit(self):
		if self.input_char in Lexer.DIGITS:
			self.next_char()
			return True

		return False
	
	# Production rule: [Letter|D]* -> a|b|c|...|x|y|z|A|B|C|...|X|Y|Z|_|0|1|3|...|7|8|9|ε|[Letter|D]* [Letter|D]*
	def letter_or_digit(self):
	# Follow([Letter|D]*) = {=,*,+,-,;,)} teriminating case
		if self.input_char in '=*+-;)':
			return True

		if self.input_char in Lexer.ALPHABETS_:
			self.next_char()
			return self.letter_or_digit()

		return False

	# Production rule: D* -> 0|1|2|...|7|8|9|ε|DD
	def zero_or_more_digit(self):
	# Follow(D*) = {*,+,-,;,)} teriminating case
		if self.input_char in '*+-;)':
			return True

		if self.digit():
			return self.zero_or_more_digit()

		return False
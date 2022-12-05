from toy_tokens import Token, TokenType

class Lexer():
	input_char: str = ''
	current_index: int = 0
	statement: str = ''
	token_start: int = 0
	tokens: list[Token] = []
	identifier_flag = False
	literal_flag = False

	# points the input_token to the next char
	# returns the $ if it reaches the end of the string
	# creates tokens during the recursive descent parsing for syntax checking
	def next_char(self):
		if self.current_index >= len(self.statement):
			self.input_char = '$'
		else:
			self.input_char = self.statement[self.current_index]
			# create tokens
			# First(Literal) = {0,1,2,3,4,5,6,7,8,9}
			# When a literal begins
			if self.input_char in '0123456789' and self.literal_flag == False and self.identifier_flag == False:
				self.literal_flag = True
				self.token_start = self.current_index
			# Follow(Literal) = {*,+,-,;,)}
			# When a literal ends
			if self.input_char in '*+-;)' and self.literal_flag == True:
				self.literal_flag = False
				self.tokens.append(Token(TokenType.LITERAL, int(self.statement[self.token_start:self.current_index])))
			# First(I) = {a,b,c,...,x,y,z,A,B,C,...,X,Y,Z,_}
			# When an identifier begins
			if self.input_char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_' and self.identifier_flag == False:
				self.identifier_flag = True
				self.token_start = self.current_index
			# Follow(I) = {=,*,+,-,;,)}
			# When an identifier ends
			if self.input_char in '=*+-;)' and self.identifier_flag == True:
				self.identifier_flag = False
				self.tokens.append(Token(TokenType.IDENTIFIER, self.statement[self.token_start:self.current_index]))
			match self.input_char:
				case '=':
					self.tokens.append(Token(TokenType.ASSIGNMENT))
				case '-':
					self.tokens.append(Token(TokenType.MINUS))
				case '+':
					self.tokens.append(Token(TokenType.PLUS))
				case '*':
					self.tokens.append(Token(TokenType.MULTIPLY))
				case '(':
					self.tokens.append(Token(TokenType.LPAREN))
				case ')':
					self.tokens.append(Token(TokenType.RPAREN))
			print(self.input_char, end='')
			self.current_index += 1
	
	# checks current input_token to the expected_token
	# if they don't match then returns false, otherwise match advances to the next token with next_char(0) call and returns true
	def match(self, expected_char: str) -> bool:
		if self.input_char != expected_char:
			return False
		self.next_char()
		return True

	# initialize class variables and starts the parsing of passed in string
	def tokenize(self, statement: str) -> bool:
		# initialize variables
		self.statement = statement
		self.current_index = 0
		# starts parsing
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
	def assignment(self) -> bool:
		if not self.identifier():
			print('Not identifier')
			return False
		if not self.match('='):
			print('not =')
			return False
		if not self.expression():
			print('not expression')
			return False
		return self.match(';')

	# Production rule: E -> TE'
	def expression(self) -> bool:
		if not self.term():
			print('not term')
			return False
		if not self.expression_prime():
			print('not expression_prime')
			return False
		return True

	# Production rule: E' -> +TE' | -TE' | ε
	def expression_prime(self) -> bool:
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
	def term(self) -> bool:
		if not self.factor():
			return False
		if not self.term_prime():
			return False
		return True

	# Production rule: T' -> *FT' | ε
	def term_prime(self) -> bool:
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
	def factor(self) -> bool:
		# Literal
		if self.input_char in '0123456789':
			return self.literal()
		# I
		if self.input_char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
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
	def identifier(self) -> bool:
		if not self.letter():
			return False
		if not self.letter_or_digit():
			return False
		return True

	# Production rule: Letter -> a|b|c|...|x|y|z|A|B|C|...|X|Y|Z|_
	def letter(self) -> bool:
		if self.input_char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
			self.next_char()
			return True
		return False

	# Production rule: Literal -> 0 | NZ D*
	def literal(self) -> bool:
		if self.input_char == '0':
			self.next_char()
			return True
		if not self.non_zero_digit():
			return False
		if not self.zero_or_more_digit():
			return False
		return True

	# Production rule: NZ -> 1|2|3|...|7|8|9
	def non_zero_digit(self) -> bool:
		if self.input_char in '123456789':
			self.next_char()
			return True
		return False
	
	# Production rule: D -> 0|1|2|...|7|8|9
	def digit(self) -> bool:
		if self.input_char in '0123456789':
			self.next_char()
			return True
		return False
	
	# Production rule: [Letter|D]* -> a|b|c|...|x|y|z|A|B|C|...|X|Y|Z|_|0|1|3|...|7|8|9|ε|[Letter|D]* [Letter|D]*
	def letter_or_digit(self) -> bool:
	# Follow([Letter|D]*) = {=,*,+,-,;,)} teriminating case
		if self.input_char in '=*+-;)':
			return True
		if self.input_char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789':
			self.next_char()
			return self.letter_or_digit()
		return False

	# Production rule: D* -> 0|1|2|...|7|8|9|ε|DD
	def zero_or_more_digit(self) -> bool:
	# Follow(D*) = {*,+,-,;,)} teriminating case
		if self.input_char in '*+-;)':
			return True
		if self.digit():
			return self.zero_or_more_digit()
		return False

def main(statement: str):
	lexer = Lexer()
	print(lexer.tokenize(statement))
	print(lexer.getTokens())

# main('z=---(((x+y)))-(x+-1);')
# main('z=308080+982*(x+-1);')
main('z=---(x+y)*(x+-y);')
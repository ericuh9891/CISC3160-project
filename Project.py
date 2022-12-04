class Lexer():
  input_char: str
  current_index: int
  statement: str

  # points the input_token to the next char
  # returns the $ if it reaches the end of the string
  def next_char(self):
    if self.current_index >= len(self.statement):
      self.input_char = '$'
    else:
      self.input_char = self.statement[self.current_index]
      print(self.input_char)
      self.current_index += 1
  
  # checks current input_token to the expected_token
  # if they don't match then returns false, otherwise match advances to the next token with next_token call and returns true
  def match(self, expected_char: str) -> bool:
    if self.input_char != expected_char:
      return False
    self.next_char()
    return True

   # initialize class variables and starts the parsing of passed in string
  def run(self, statement: str) -> bool:
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
      case '+' | '-':
        self.next_char()
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
      case '-' | '+':
        self.next_char()
        if not self.factor():
          return False
        return True
      # I think Follow(F) = {*,+,-,;,)} aka ending chars
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
  # I think Follow([Letter|D]*) = {=,*,+,-,;,)} aka ending chars
  def letter_or_digit(self) -> bool:
    if self.input_char in '=*+-;)':
      return True
    if self.input_char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789':
      self.next_char()
      return self.letter_or_digit()
    return False

  # Production rule: D* -> 0|1|2|...|7|8|9|ε|DD
  # I think Follow(D*) = {*,+,-,;,)} aka ending chars
  def zero_or_more_digit(self) -> bool:
    if self.input_char in '*+-;)':
      return True
    if self.digit():
      return self.zero_or_more_digit()
    return False

def main(statement: str):
  print(Lexer().run(statement))

main('z=---(((x+y)))-(x+-y);')
"""
This is a Parser in python that was converted from an equivalent Java Parser for grammar:
E -> TE`
E` -> +TE` | -TE` | ε
T -> FT`
T` -> *FT` | /FT` | ε
F -> 0|1|2|3|4|5|6|7|8|9| (E)
"""


class Parser():
  input_token: str # current input token char
  index: int # pointer to keep track of the current input_token
  string: str # statement string to be parsed

  # points the input_token to the next char
  # returns the $ if it reaches the end of the string
  def next_token(self):
    if self.index >= len(self.string):
      self.input_token = '$'
    else:
      self.input_token = self.string[self.index]
      self.index += 1

  # checks current input_token to the expected_token
  # if they don't match then returns false, otherwise match advances to the next token with next_token call and returns true
  def match(self, expected_token: str) -> bool: 
    if self.input_token != expected_token:
      return False
    self.next_token()
    return True

  # initialize class variables and starts the parsing of passed in string
  def parser(self, sen: str) -> bool:
    # initialize variables
    self.string = sen
    self.index = 0
    # starts parsing
    self.next_token()
    if not self.exp():
      return False
    # if exp is true and the last char is $ then expression was valid and returns true
    return self.match('$')

  # Production rule: E -> TE`
  # if first token is T (term) and the next is E` (exp_prime) then it is an expression (exp) and returns true
  def exp(self) -> bool:
    if not self.term():
      return False
    if not self.exp_prime():
      return False
    return True

  # Production rule: E` -> +TE` | -TE` | ε
  def exp_prime(self) -> bool:
    match self.input_token:
      case '+' | '-':
        self.next_token()
        if not self.term():
          return False
        if not self.exp_prime():
          return False
        return True
      case '$' | ')':
        return True
      case _:
        return False

  # Production rule: T -> FT`
  def term(self) -> bool:
    if not self.factor():
      return False
    if not self.term_prime():
      return False
    return True
  
  # Production rule: T` -> *FT` | /FT` | ε
  def term_prime(self) -> bool:
    match self.input_token:
      case '*' | '/':
        self.next_token()
        if not self.factor():
          return False
        if not self.term_prime():
          return False
        return True
      case '+' | '-' | ')' | '$':
        return True
      case _:
        return False

  # Production rule: F -> 0|1|2|3|4|5|6|7|8|9| (E)
  def factor(self) -> bool:
    match self.input_token:
      case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
        self.next_token()
        self.factor() # not part of grammar, this added call allows for unlimited number of digits
        return True
      case '(':
        self.next_token()
        if not self.exp():
          return False
        return self.match(')')
      case _:
        return False

def main():
  print(Parser().parser('4-31+22231*(123)'))

main()
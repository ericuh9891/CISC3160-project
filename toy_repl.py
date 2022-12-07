from toy_lexer import Lexer
from toy_parser import Parser
from toy_interpreter import Interpreter

variables = {}

while True:
  try:
    statement = input("toyREPL> ")
    lexer = Lexer(statement)
    print(f"Lexer: {lexer}")
    # lexer.tokenize(statement)
    tokens = lexer.getTokens()
    # temp hack to test the parser
    # tokens = tokens[2:len(tokens)]
    print(f"Tokens: {tokens}")
    parser = Parser(tokens)
    tree = parser.parse()
    print(f"Tree: {tree}")
    if not tree: continue
    interpreter = Interpreter(variables)
    variable, value = interpreter.visit(tree)
    print(f"Evaluated variable and value: {variable}, {value}")
    variables[variable] = value
    print(f"Saved Variables: {variables}")
  except Exception as e:
    raise e
from toy_lexer import Lexer
from toy_parser import Parser
from toy_interpreter import Interpreter

variables = {}

while True:
  try:
    statement = input("toyREPL> ")
    lexer = Lexer(statement)
    print(f"Lexer: {lexer}")
    tokens = lexer.getTokens()
    parser = Parser(tokens)
    tree = parser.parse()
    print(f"Tree: {tree}")
    if not tree: continue
    interpreter = Interpreter(variables)
    variable, value = interpreter.visit(tree)
    print(f"Evaluated variable and value: {variable}, {value}")
    variables[variable] = value
    print(f"Saved Variables: {variables}")
  except KeyboardInterrupt:
    print("Exiting")
    exit()
  except SyntaxError as se:
    print(f"Syntax Error" + f"" if se else f" {se}")
  except Exception as e:
    raise e
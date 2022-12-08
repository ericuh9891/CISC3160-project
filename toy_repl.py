from toy_lexer import Lexer
from toy_parser import Parser
from toy_interpreter import Interpreter

variables = {}

while True:
  try:
    statement = input("toyREPL> ")

    lexer = Lexer(statement)

    parser = Parser(lexer.getTokens(), variables)
    tree = parser.parse()
    if not tree: continue
    
    interpreter = Interpreter(variables)
    variable, value = interpreter.visit(tree)
    variables[variable] = value

    print(f"{variable} = {value}")

  except KeyboardInterrupt:
    print("Exiting")
    exit()

  except SyntaxError as se:
    print(f"Syntax Error:")
    continue

  except NameError as ne:
    print(f"Uninitialized Error: {ne}")
    continue

  except Exception as e:
    raise e
from toy_lexer import Lexer
from toy_parser import Parser
from toy_interpreter import Interpreter
import sys

def main():
  variables = {}
  output = []
  line_counter = 1

  # Read and parse file
  try:
    file = open(sys.argv[1],"r")
    lines = file.readlines()

  except Exception as e:
    raise e

  # parse and evaluate each line
  try:
    for line in lines:
      new_line_removed = line.replace("\n", "")
      space_removed = new_line_removed.replace(" ", "")

      statement = space_removed

      lexer = Lexer(statement)

      parser = Parser(lexer.getTokens(), variables)
      tree = parser.parse()
      if not tree: continue
      
      interpreter = Interpreter(variables)
      variable, value = interpreter.visit(tree)
      variables[variable] = value

      output.append(f"{variable} = {value}")

      line_counter += 1

  except SyntaxError:
    output.append(f"Syntax Error on line {line_counter} : {new_line_removed}")

  except NameError as ne:
    output.append(f"Uninitialized Error on line {line_counter} : '{new_line_removed}' : {ne}")

  except Exception as e:
    raise e
  
  # print all results
  for result in output:
    print(result)

if __name__ == "__main__":
  main()
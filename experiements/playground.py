
def main():
	try:
		while True:
			statement = input("repl> ")
			print(statement)
	except KeyboardInterrupt:
		exit()

def test1():
	if "":
		print("Empty string is evaluates to true")
# main()
test1()
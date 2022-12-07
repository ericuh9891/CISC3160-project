
def main():
	variables = {'x':1}
	variables[3] = 2
	print(variables)
	testGet = variables.get('z')
	print(testGet)
	emptyDict = {}
	print(f"bool dict test: {not bool(emptyDict)}")
main()
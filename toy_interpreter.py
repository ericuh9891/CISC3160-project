from toy_nodes import *
from toy_number import Number

class Interpreter:
	variables: dict[str, int]

	def __init__(self, variables):
		self.variables = variables

	def visit(self, node):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name)
		return method(node)

	def visit_AssignmentNode(self, node):
		return (self.visit(node.node_a).value, self.visit(node.node_b).value)

	def visit_IdentifierNode(self, node):
		print(f"IdentifierNode: {node.value}, get variable: {self.variables.get(node.value)}")
		if bool(self.variables) and self.variables.get(node.value) != None:
			return Number(self.variables.get(node.value))
		else:
			return Number(node.value)

	def visit_NumberNode(self, node):
		return Number(node.value)

	def visit_AddNode(self, node):
		return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)

	def visit_SubtractNode(self, node):
		return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

	def visit_MultiplyNode(self, node):
		return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)
	
	def visit_PlusNode(self, node):
		return self.visit(node.node)

	def visit_MinusNode(self, node):
		print(f'visit_MinusNode: {node}')
		return Number(-self.visit(node.node).value)
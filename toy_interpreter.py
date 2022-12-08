from toy_nodes import *

class Interpreter:
	variables: dict[str, int]

	def __init__(self, variables):
		self.variables = variables

	def visit(self, node):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name)
		return method(node)

	def visit_AssignmentNode(self, node):
		return (self.visit(node.node_a), self.visit(node.node_b))

	def visit_IdentifierNode(self, node):
		return node.value

	def visit_NumberNode(self, node):
		return node.value

	def visit_AddNode(self, node):
		return self.visit(node.node_a) + self.visit(node.node_b)

	def visit_SubtractNode(self, node):
		return self.visit(node.node_a) - self.visit(node.node_b)

	def visit_MultiplyNode(self, node):
		return self.visit(node.node_a) * self.visit(node.node_b)
	
	def visit_PlusNode(self, node):
		return self.visit(node.node)

	def visit_MinusNode(self, node):
		return -self.visit(node.node)
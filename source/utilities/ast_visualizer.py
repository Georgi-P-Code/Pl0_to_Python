

class Ast_visualizer:

	def __init__(self, ast):
		self.ast = ast
		self.indentation_level = 0


	def visualize(self):
		self.result = ""
		self.visit(self.ast)
		return self.result[:-1] # removes the last \n char


	def new_line(self):
		a = self.indentation_level * '   '
		if self.indentation_level == 0:
			return ""
		else:
			return f"{a[:-3]}└──"


	def result_add_line(self, line):
		self.result += f'{self.new_line()}{str(line)}\n'


	def parse_item(self, node_name, node_body):
		self.result_add_line(node_name)
		self.indentation_level += 1
		self.visit(node_body)
		self.indentation_level -= 1


	def visit(self, node):

		if type(node) == dict:
			if len(node.items()) == 1:
				node_name, node_body = self.view_node(node)

				if node_name in ["identifier", "number"]:
					self.result_add_line(node_body)

				elif node_name == "binary_operation":
					self.result_add_line(node_body['operation'])
					self.indentation_level += 1
					self.visit(node_body["left"])
					self.visit(node_body["right"])
					self.indentation_level -= 1

				elif node_name == "assignment":
					self.result_add_line("assignment")
					self.indentation_level += 1
					self.visit(node_body["left"])
					self.visit(node_body["right"])
					self.indentation_level -= 1

				elif node_name == "condition":
					if node_body.get("odd"):
						self.result_add_line("odd")
						self.indentation_level += 1
						self.visit(node_body["odd"])
						self.indentation_level -= 1
					else:
						self.result_add_line(node_body['operation'])
						self.indentation_level += 1
						self.visit(node_body["left"])
						self.visit(node_body["right"])
						self.indentation_level -= 1

				else:
					self.parse_item(node_name, node_body)

			elif len(node.items()) > 1:
				list_of_nodes = self.view_multiple_pair_node(node)

				for (node_name, node_body) in list_of_nodes:
					self.visit({node_name: node_body})

			else:
				assert False, f"Got dict with {len(node.items())} items."

		elif type(node) == list:
			for child_node in node:
				self.visit(child_node)

		elif type(node) in [str, int, type(None)]:
			self.result_add_line(node)

		else:
			assert False, f"Unknown node type ({type(node)})"


	def view_multiple_pair_node(self, node):
		return list(node.items())


	def view_node(self, node):
		node_name =  list(node.keys())[0]
		node_body = node[node_name]
		return node_name, node_body

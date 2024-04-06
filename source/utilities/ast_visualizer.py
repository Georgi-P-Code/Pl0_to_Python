

class Ast_visualizer:

	def __init__(self, ast):
		self.ast = ast
		self.indent = 0

	def get_info(self, node):
		node_name = list(node.keys())[0]
		node_value = list(node.values())[0]
		return (node_name, node_value)

	def visualize(self):
		# left: str, right: dict[k, v one]
		# left: dict, right, dict
		# left: str, right: list
		# left: str, right: dict[k, v many]
		# left: str, right: str | number
		return self.visualize_(self.ast)

	def visualize_(self, node):
		node_name, node_value = self.get_info(node)

		if type(node_value) in [str, int, float]:
			return f'{node_name}:\n\t{node_value}'

		if type(node_value) == list:
			out = "LIST<"
			for value in node_value:
				out += self.visualize_(value)+", "

			return out+">"

		if type(node_value) == dict:
			self.indent += 1
			ident_level = self.indent * "\t"
			return f'{node_name}:\n{ident_level}{self.visualize_(node_value)}'

		raise Exception(f"Don't how to visualize -> {node_name}: {node_value}")
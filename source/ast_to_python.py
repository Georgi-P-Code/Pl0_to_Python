
class Translation_error(Exception): pass

class Translator:

    def __init__(self, ast: dict):
        self.ast = ast


    def translate(self):
        self.constants = []
        self.variables = []
        self.indentation_level = 0

        return self.evaluate(self.ast)


    def evaluate(self, node):
        #print("Evaluateing:", node)
        number_of_children = None#TODO
        node_type = str(list(node.keys())[0])
        #print("Evaluateing:", node_type)
        #print(type(node_type))

        result = None

        match node_type:
            case "program":
                result = self.evaluate_program(node)

            case "block":
                result = self.evaluate_block(node)

            case "constant_declarations":
                result = self.evaluate_constant_declarations(node)

            case "constant_declaration":
                result = self.evaluate_constant_declaration(node)

            case "variable_declarations":
                result = self.evaluate_variable_declarations(node)

            case "begin_block":
                result = self.evaluate_begin_block(node)

            case "while_loop":
                self.indent()
                result = self.evaluate_while_loop(node)
                self.undent()

            case "loop_condition":
                result = self.evaluate_loop_condition(node)

            case "loop_statement":
                result = self.evaluate_loop_statement(node)

            case "statement":
                result = self.evaluate_statement(node)

            case "binary_operation":
                result = self.evaluate_binary_operation(node)

            case "assignment":
                result = self.evaluate_assignment(node)

            case "identifier":
                result = self.evaluate_identifier(node)

            case "number":
                result = self.evaluate_number(node)

            case "term":
                #return
                raise Exception("TODO term") #'":)"'

            case _:
                raise Exception(f"Don't know how to evaluate node of type \"{node_type}\"")

        return result


    def evaluate_program(self, node):
        child_node = self.get_value(node)
        return self.evaluate(child_node)


    def evaluate_block(self, node):
        child_node = self.get_value(node)

        block_components = []

        for node_name, node in child_node.items():
            new_node = {node_name: node}
            #print("new node", new_node)
            evaluation = self.evaluate(new_node)
            if evaluation != "":
                block_components.append(evaluation)

        out = self.indented_new_line().join(block_components)

        return out


    def evaluate_constant_declarations(self, node):
        list_of_declarations = self.get_value(node)
        out = "constants = {"

        declarations = []

        for constant_declaration in list_of_declarations:
            declarations.append(self.evaluate(constant_declaration))

        out += ", ".join(declarations)

        return out + "}"


    def evaluate_variable_declarations(self, node):
        list_of_variables = self.get_value(node)
        out = ""

        declarations = []

        for variable in list_of_variables:
            # variable_name = self.get_value(variable)
            #
            # if variable_name in self.variables:
            #     self.translation_error(f'Variable with name "{variable_name}" has already been declared.')

            variable_name = self.evaluate(variable)

            thing = f'{variable_name} = None'
            declarations.append(thing)

            #self.variables.append(variable_name)

        out += self.indented_new_line().join(declarations)

        return ""#out


    def evaluate_constant_declaration(self, node):
        child_node = self.get_value(node)
        left_node = child_node["left"]
        right_node = child_node["right"]

        identifier_name = self.evaluate(left_node)

        self.constants.append(identifier_name)

        return f'"{identifier_name}" = {self.evaluate(right_node)}'


    def evaluate_statement(self, node):
        child_node = self.get_value(node)
        return self.evaluate(child_node)


    def evaluate_begin_block(self, node):
        child_node = self.get_value(node)

        out = ""

        begin_block_components = []

        for statement in child_node:
            begin_block_components.append( self.evaluate(statement) )

        out = self.indented_new_line().join(begin_block_components)

        return out


    def evaluate_while_loop(self, node):
        child_node = self.get_value(node)

        #print( str(self.get_info(self.get_value(child_node["loop_condition"]))) )

        loop_condition = self.evaluate( {"loop_condition": child_node["loop_condition"]} )
        loop_statement = self.evaluate( {"loop_statement": child_node["loop_statement"]} )

        out = f"while {loop_condition}:"\
              f"{self.indented_new_line()}{loop_statement}"

        return out


    def evaluate_loop_condition(self, node):
        child_node = self.get_value(node)

        operation = child_node["operation"]
        left = self.evaluate( child_node["left"] )
        right = self.evaluate( child_node["right"] )

        return f"{left} {operation} {right}"


    def evaluate_loop_statement(self, node):
        child_node = self.get_value(node)

        print(self.get_info(child_node))

        return self.evaluate(child_node)


    def evaluate_binary_operation(self, node):
        child_node = self.get_value(node)

        operation = child_node["operation"]
        left = self.evaluate( child_node["left"] )
        right = self.evaluate( child_node["right"] )

        print(self.get_info(child_node))

        return f"{left} {operation} {right}"


    def evaluate_assignment(self, node):
        #print("???", node)
        child = self.get_value(node)
        #print("??? child", child)
        left = self.evaluate(child["left"])
        right = self.evaluate(child["right"])

        return f"{left} = {right}"


    def evaluate_identifier(self, node):
        identifier_name = self.get_value(node)

        if identifier_name in self.constants:
            identifier_name = f'constants["{identifier_name}"]'

        # elif identifier_name in self.variables:
        #     identifier_name = f'variable["{identifier_name}"]'

        return identifier_name


    def evaluate_number(self, node):
        return str(self.get_value(node))


    def get_value(self, node):
        assert type(node) == dict, f'Expected dict but got string "{node}"'
        node_values = node.values()
        #assert len(node_values) == 1
        return list(node_values)[0]


    def get_values(self, node):
        assert type(node) == dict, f'Expected dict but got string "{node}"'
        node_values = node.values()
        assert len(node_values) != 1
        return list(node_values)


    def get_first_child(self, node):
        assert type(node) == dict, f'Expected dict but got string "{node}"'
        return node[list(node.keys())[0]]


    def get_child(self, node):
        assert type(node) == dict, f'Expected dict but got string "{node}"'
        return


    def get_info(self, node):
        out = {}

        out["node_type"] = type(node)

        if out["node_type"] == dict:
            #out["node_name"] = list(node.keys())[0]
            out["node keys"] = list(node.keys())
            #out["value_type"] = type(list(node.values())[0])

        elif out["node_type"] == str:
            out["value"] = node

        return out

    def translation_error(self, message: str):
        raise Translation_error(message)

        # current_token = self.current_token()
        # error_snippet = self.original_text.split("\n")[current_token.line_number - 1]
        #
        # raise Translation_error(
        #     f'\n\t{error_snippet}\n'
        #     f"Line {current_token.line_number}: {message}\n"
        #     f"In position {self.position} for {current_token}"
        # )


    def indent(self):
        self.indentation_level += 1


    def undent(self):
        self.indentation_level -= 1


    def indentation(self):
        return "\t" * self.indentation_level


    def indented_new_line(self):
        return "\n"+self.indentation()

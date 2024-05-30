
from exceptions import Translation_error

# constant_class = """\
# class Constant:
#     def __init__(self, **kvargs):
#         self.constants = kvargs
#
#     def __getitem__(self, item):
#         return self.constants[item]
#
#     def __setitem__(self, name, value):
#         raise Exception(f'Attempt to change "{name}" a constant value.')\n\n
# """


class Translator:

    def __init__(self, ast: dict, scope_information):
        self.ast = ast
        self.scope = scope_information
        self.current_scope = None
        self.previous_scope = None
        self.visited_scopes = {}
        self.identifiers_used_throughout_procedure = {}


    def translate(self) -> str:
        self.constants = []
        self.variables = []
        self.indentation_level = 0

        #self.prepend_constants_class = False

        output = self.evaluate(self.ast)

        # if self.prepend_constants_class:
        #     output = constant_class + output

        return output


    def evaluate(self, node) -> str:
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

            case "procedure_definitions":
                self.indent()
                result = self.evaluate_procedure_definitions(node)
                self.undent()

            case "begin_block":
                result = self.evaluate_begin_block(node)

            case "if":
                self.indent()
                result = self.evaluate_if_statement(node)
                self.undent()

            case "while_loop":
                self.indent()
                result = self.evaluate_while_loop(node)
                self.undent()

            case "condition":
                result = self.evaluate_condition(node)

            case "statement":
                result = self.evaluate_statement(node)

            case "call":
                result = self.evaluate_call(node)

            case "exclamation":
                result = self.evaluate_exclamation(node)

            case "binary_operation":
                result = self.evaluate_binary_operation(node)

            case "assignment":
                result = self.evaluate_assignment(node)

            case "identifier":
                result = self.evaluate_identifier(node)

            case "number":
                result = self.evaluate_number(node)

            case "empty_statement":
                result = self.evaluate_empty_statement(node)

            case _:
                raise Exception(f"Don't know how to evaluate node of type \"{node_type}\"")

        return result


    def evaluate_program(self, node):
        child_node = self.get_value(node)
        return self.evaluate(child_node)


    def evaluate_block(self, node):
        child_node = self.get_value(node)

        self.enter_scope()

        block_components = []
        #list_of_used_variable_names = []

        for node_name, node in child_node.items():
            evaluation = self.evaluate({node_name: node})

            if evaluation != "":
                block_components.append(evaluation)

        out = self.indented_new_line().join(block_components)

        self.leave_scope()

        return out#, list_of_used_variable_names


    def evaluate_constant_declarations(self, node):
        #self.prepend_constants_class = True

        list_of_declarations = self.get_value(node)

        declarations = []

        for constant_declaration in list_of_declarations:
            declarations.append(self.evaluate(constant_declaration))

        constants_list = "; ".join(declarations)

        return f"{constants_list}"


    def evaluate_variable_declarations(self, node):
        list_of_variables = self.get_value(node)
        out = ""

        declarations = []

        for variable in list_of_variables:
            variable_name = self.get_value(variable)

            # if variable_name in self.variables:
            #     self.translation_error(f'Variable with name "{variable_name}" has already been declared.')

            variable_name = self.evaluate(variable)

            declarations.append(f'{variable_name} = None')

            self.variables.append(variable_name)

        out += self.indented_new_line().join(declarations) + self.indented_new_line()

        return out


    def evaluate_procedure_definitions(self, node):
        list_of_procedure_definitions = self.get_value(node)

        list_of_procedure_definition_results = []

        for procedure_definition in list_of_procedure_definitions:
            procedure_name = self.evaluate(procedure_definition["procedure_name"])
            self.identifiers_used_throughout_procedure = {}
            procedure_body = self.evaluate(procedure_definition["procedure_body"])

            #print(f"USED {self.identifiers_used_throughout_procedure}")

            identifiers_from_outer_scope = []
            for identifier_name in self.identifiers_used_throughout_procedure.keys():
                #print(f'IS "{identifier_name}" IN CURRENT SCOPE?')
                #print(self.current_scope.identifiers)
                if not self.was_in_scope(identifier_name):
                    identifiers_from_outer_scope.append(identifier_name)

            if identifiers_from_outer_scope:
                if_global_variables = f'{self.indented_new_line()}global {", ".join(identifiers_from_outer_scope)}'
            else:
                if_global_variables = ""

            definition_str = f'def {procedure_name}():'\
                             f'{if_global_variables}' \
                             f'{self.indented_new_line()}{procedure_body}\n'

            list_of_procedure_definition_results.append(definition_str)

        return "\n".join(list_of_procedure_definition_results)


    def evaluate_constant_declaration(self, node):
        child_node = self.get_value(node)
        left_node = child_node["left"]
        right_node = child_node["right"]

        identifier_name = self.evaluate(left_node)

        self.constants.append(identifier_name)

        return f'{identifier_name} = {self.evaluate(right_node)}'


    def evaluate_statement(self, node):
        child_node = self.get_value(node)
        return self.evaluate(child_node)


    def evaluate_call(self, node):
        child_node = self.get_value(node)
        return f"{self.evaluate(child_node)}()"


    def evaluate_exclamation(self, node):
        child_node = self.get_value(node)
        return f"print({self.evaluate(child_node)})"


    def evaluate_begin_block(self, node):
        child_node = self.get_value(node)

        out = ""

        begin_block_components = []

        for statement in child_node:
            begin_block_components.append( self.evaluate(statement) )

        out = self.indented_new_line().join(begin_block_components)

        return out


    def evaluate_if_statement(self, node):
        child_node = self.get_value(node)

        condition = self.evaluate( {"condition": child_node["condition"]} )
        statement = self.evaluate( {"statement": child_node["statement"]} )

        out = f'if {condition}:' \
              f'{self.indented_new_line()}{statement}'

        return out


    def evaluate_while_loop(self, node):
        child_node = self.get_value(node)

        #print( str(self.get_info(self.get_value(child_node["loop_condition"]))) )

        loop_condition = self.evaluate( {"condition": child_node["condition"]} )
        loop_statement = self.evaluate( {"statement": child_node["statement"]} )

        out = f"while {loop_condition}:"\
              f"{self.indented_new_line()}{loop_statement}"

        return out


    def evaluate_condition(self, node):
        child_node = self.get_value(node)

        if child_node.get("odd"):
            expression = self.evaluate( child_node["odd"] )
            return f'({expression})%2 != 0'

        operation = child_node["operation"]

        if operation == "=":
            operation = "=="

        elif operation == "#":
            operation = "!="

        left = self.evaluate( child_node["left"] )
        right = self.evaluate( child_node["right"] )

        return f"{left} {operation} {right}"


    def evaluate_binary_operation(self, node):
        child_node = self.get_value(node)

        operation = child_node["operation"]
        left = self.evaluate( child_node["left"] )
        right = self.evaluate( child_node["right"] )

        #print(self.get_info(child_node))

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

        result = self.current_scope.is_visible(identifier_name)
        identifier_type = result[identifier_name]

        if identifier_type != "procedure":
        #     if not self.identifiers_used_throughout_procedure.get(identifier_name):
        #         print(f"ADDING {identifier_name} {identifier_type}")
            self.identifiers_used_throughout_procedure[identifier_name] = True
        # else:
        #     print(f"SKIPPING {identifier_name} {identifier_type}")

        if identifier_name in self.constants:
            identifier_name = f'{identifier_name}'

        # elif identifier_name in self.variables:
        #     identifier_name = f'variable["{identifier_name}"]'

        return identifier_name

    def evaluate_empty_statement(self, node):
        return "pass"

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


    def enter_scope(self):
        if self.current_scope is None:
            self.current_scope = self.scope
            self.visited_scopes[f"Level {self.current_scope.level}"] = 1
        else:
            try:
                inner_scope_position = self.visited_scopes[f"Level {self.current_scope.level + 1}"]
            except KeyError:
                self.visited_scopes[f"Level {self.current_scope.level + 1}"] = 1
                inner_scope_position = 1

            self.previous_scope = self.current_scope
            self.current_scope = self.current_scope.inner[inner_scope_position-1]


            self.visited_scopes[f"Level {self.current_scope.level}"] += 1



        #print(f"ast_to_py: Enter scope {self.current_scope.name} (Level {self.current_scope.level})")


    def leave_scope(self):
        #print(f"ast_to_py: Leave scope {self.current_scope.name} (Level {self.current_scope.level})")
        before_change = self.previous_scope
        if before_change is None:
            before_change_name = "<empty>"
        else:
            before_change_name = before_change.name
        self.previous_scope = self.current_scope
        #print(f'previous scope: {before_change_name} -> {self.previous_scope.name}')

        before_change_cs = self.current_scope
        if before_change_cs is None:
            before_change_cs_name = "<empty>"
        else:
            before_change_cs_name = before_change_cs.name
        #print(f"ast_to_py: Leaving scope {self.current_scope.name} (Level {self.current_scope.level})")
        self.current_scope = self.current_scope.parent
        cp_name = self.current_scope.name if self.current_scope is not None else "<empty>"
        #print(f'current scope: {before_change_cs_name} -> {cp_name}')


    def was_in_scope(self, identifier_name: str):
        return self.previous_scope.identifiers.get(identifier_name)


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

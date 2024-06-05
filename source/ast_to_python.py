

class Translator:

    def __init__(self, ast: dict, scope_information):
        self.ast = ast
        self.scope = scope_information
        self.current_scope = None
        self.previous_scope = None
        self.visited_scopes = {}
        self.identifiers_used_throughout_procedure = {}


    def translate(self) -> str:
        self.indentation_level = 0
        return self.evaluate(self.ast)


    def evaluate(self, node) -> str:
        node_type = str(list(node.keys())[0])

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

            case "question_mark":
                result = self.evaluate_question_mark(node)

            case "binary_operation":
                result = self.evaluate_binary_operation(node)

            case "unary_operation":
                result = self.evaluate_unary_operation(node)

            case "assignment":
                result = self.evaluate_assignment(node)

            case "expression":
                result = self.evaluate_expression(node)

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
        for node_name, node in child_node.items():
            evaluation = self.evaluate({node_name: node})

            if evaluation != "":
                block_components.append(evaluation)

        out = self.indented_new_line().join(block_components)

        self.leave_scope()

        return out


    def evaluate_constant_declarations(self, node):
        list_of_declarations = self.get_value(node)
        declarations = []

        for constant_declaration in list_of_declarations:
            declarations.append(self.evaluate(constant_declaration))

        constants_list = "; ".join(declarations)

        return constants_list


    def evaluate_variable_declarations(self, node):
        list_of_variables = self.get_value(node)
        out = ""
        declarations = []

        for variable in list_of_variables:
            variable_name = self.evaluate(variable)
            declarations.append(f'{variable_name} = None')

        out += self.indented_new_line().join(declarations) + self.indented_new_line()

        return out


    def evaluate_procedure_definitions(self, node):
        list_of_procedure_definitions = self.get_value(node)

        list_of_procedure_definition_results = []

        for procedure_definition in list_of_procedure_definitions:
            procedure_name = self.evaluate(procedure_definition["procedure_name"])
            self.identifiers_used_throughout_procedure = {}
            procedure_body = self.evaluate(procedure_definition["procedure_body"])

            identifiers_from_outer_scope = []
            for identifier_name in self.identifiers_used_throughout_procedure.keys():
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

        identifier_name = self.evaluate(child_node["left"])
        number = self.evaluate(child_node["right"])

        return f'{identifier_name} = {number}'


    def evaluate_statement(self, node):
        child_node = self.get_value(node)
        return self.evaluate(child_node)


    def evaluate_call(self, node):
        child_node = self.get_value(node)
        return f"{self.evaluate(child_node)}()"


    def evaluate_exclamation(self, node):
        child_node = self.get_value(node)
        return f"print({self.evaluate(child_node)})"


    def evaluate_question_mark(self, node):
        child_node = self.get_value(node)
        identifier_name = self.evaluate(child_node)
        return f'print(f"{identifier_name} = {{{identifier_name}}}")'


    def evaluate_begin_block(self, node):
        child_node = self.get_value(node)

        begin_block_components = []

        for statement in child_node:
            begin_block_components.append( self.evaluate(statement) )

        return self.indented_new_line().join(begin_block_components)


    def evaluate_if_statement(self, node):
        child_node = self.get_value(node)

        condition = self.evaluate( {"condition": child_node["condition"]} )
        statement = self.evaluate( {"statement": child_node["statement"]} )

        out = f'if {condition}:' \
              f'{self.indented_new_line()}{statement}'

        return out


    def evaluate_while_loop(self, node):
        child_node = self.get_value(node)

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

        return f"{left} {operation} {right}"


    def evaluate_unary_operation(self, node):
        child_node = self.get_value(node)

        operation = child_node["operation"]
        left = self.evaluate( child_node["left"] )

        return f"{operation}{left}"


    def evaluate_assignment(self, node):
        child = self.get_value(node)
        left = self.evaluate(child["left"])
        right = self.evaluate(child["right"])

        return f"{left} = {right}"


    def evaluate_expression(self, node):
        child = self.get_value(node)
        expression = self.evaluate(child)

        return f"({expression})"


    def evaluate_identifier(self, node):
        identifier_name = self.get_value(node)

        result = self.current_scope.is_visible(identifier_name)
        identifier_type = result[identifier_name]

        if identifier_type != "procedure":
            self.identifiers_used_throughout_procedure[identifier_name] = True

        return identifier_name


    def evaluate_empty_statement(self, node):
        return "pass"


    def evaluate_number(self, node):
        return str(self.get_value(node))


    def get_value(self, node):
        assert type(node) == dict, f'Expected dict but got string "{node}"'
        node_values = node.values()
        return list(node_values)[0]


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


    def leave_scope(self):
        self.previous_scope = self.current_scope
        self.current_scope = self.current_scope.parent


    def was_in_scope(self, identifier_name: str):
        return self.previous_scope.identifiers.get(identifier_name)


    def indent(self):
        self.indentation_level += 1


    def undent(self):
        self.indentation_level -= 1


    def indentation(self):
        return "\t" * self.indentation_level


    def indented_new_line(self):
        return "\n"+self.indentation()

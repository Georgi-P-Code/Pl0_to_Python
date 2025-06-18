from parser import Parser
from token_type import Token_type
from exceptions import Invalid_syntax


class Pl0_parser_v1(Parser):

    def parse(self):
        ast = self.program()
        self.match(Token_type.EOF)

        return ast


    def program(self):
        ast = self.block()
        self.match(Token_type.DOT)

        return {"program": ast}


    def block(self):
        ast = {}

        self.new_scope()

        if self.check_token(Token_type.KEYWORD, "const"):
            self.position += 1

            constant_declarations = []

            identifier_name = self.match(Token_type.IDENTIFIER).value
            self.add_identifier_to_current_scope(identifier_name, "constant")
            self.match(Token_type.EQUALS)
            number = self.match(Token_type.NUMBER).value

            constant_declarations.append({
                "constant_declaration": {
                    "left": {"identifier": identifier_name},
                    "right": {"number": number}
                }
            })

            while self.check_token(Token_type.COMMA):
                self.position += 1
                identifier_name = self.match(Token_type.IDENTIFIER).value
                self.add_identifier_to_current_scope(identifier_name, "constant")
                self.match(Token_type.EQUALS)
                number = self.match(Token_type.NUMBER).value

                constant_declarations.append({
                    "constant_declaration": {
                        "left": {"identifier": identifier_name},
                        "right": {"number": number}
                    }
                })

            self.match(Token_type.SEMICOLON)

            ast["constant_declarations"] = constant_declarations

        if self.check_token(Token_type.KEYWORD, "var"):
            self.position += 1

            variable_declarations = []

            identifier_name = self.match(Token_type.IDENTIFIER).value
            self.add_identifier_to_current_scope(identifier_name, "variable")

            variable_declarations.append({"identifier": identifier_name})

            while self.check_token(Token_type.COMMA):
                self.position += 1

                identifier_name = self.match(Token_type.IDENTIFIER).value
                self.add_identifier_to_current_scope(identifier_name, "variable")
                variable_declarations.append({"identifier": identifier_name})

            self.match(Token_type.SEMICOLON)

            ast["variable_declarations"] = variable_declarations

        while self.check_token(Token_type.KEYWORD, "procedure"):
            self.position += 1

            if not ast.get("procedure_definitions"):
                ast["procedure_definitions"] = []

            identifier_name = self.match(Token_type.IDENTIFIER).value
            self.add_identifier_to_current_scope(identifier_name, "procedure")
            self.match(Token_type.SEMICOLON)

            block_ast = self.block()

            self.match(Token_type.SEMICOLON)

            ast["procedure_definitions"].append({
                "procedure_name": {"identifier": identifier_name},
                "procedure_body": block_ast
            })

        ast["statement"] = self.statement()

        self.exit_scope()

        return {"block": ast}


    def statement(self):

        if self.check_token(Token_type.IDENTIFIER):
            self.check_if_current_identifier_name_is_declared()
            identifier_name = self.match(Token_type.IDENTIFIER).value
            self.check_if_trying_to_change_a_constant(identifier_name)
            self.match(Token_type.ASSIGNMENT)
            right_ast = self.expression()

            return {"assignment": {
                "left": {"identifier": identifier_name},
                "right": right_ast
            }}

        if self.check_token(Token_type.KEYWORD, "begin"):
            self.position += 1

            statement_list = []

            ast1 = self.statement()

            statement_list.append(ast1)

            while self.check_token(Token_type.SEMICOLON):
                self.position += 1

                ast2 = self.statement()

                statement_list.append(ast2)

            self.match(Token_type.KEYWORD, "end")

            return {"begin_block": statement_list}

        if self.check_token(Token_type.KEYWORD, "if"):
            self.position += 1

            condition = self.condition()

            self.match(Token_type.KEYWORD, "then")

            statement = self.statement()

            return {"if": {
                "condition": condition,
                "statement": statement
            }}

        if self.check_token(Token_type.KEYWORD, "while"):
            self.position += 1

            condition = self.condition()

            self.match(Token_type.KEYWORD, "do")

            statement = self.statement()

            return {"while_loop": {
                "condition": condition,
                "statement": statement
            }}

        if self.check_token(Token_type.KEYWORD, "call"):
            self.position += 1

            self.check_if_current_identifier_name_is_declared()
            identifier_name = self.match(Token_type.IDENTIFIER).value

            return {"call": {"identifier": identifier_name}}

        if self.check_token(Token_type.EXCLAMATION):
            self.position += 1

            expression_ast = self.expression()

            return {"exclamation": expression_ast}

        if self.check_token(Token_type.QUESTION_MARK):
            self.position += 1

            self.check_if_current_identifier_name_is_declared()
            identifier_name = self.match(Token_type.IDENTIFIER).value

            return {"question_mark": {"identifier": identifier_name}}

        return {"empty_statement": None}


    def condition(self):

        if self.check_token(Token_type.KEYWORD, "odd"):
            self.position += 1

            expression_ast = self.expression()

            return {"odd": expression_ast}

        ast = self.expression()
        operation = self.comparison_operation()
        ast2 = self.expression()

        return {
            "operation": operation,
            "left": ast,
            "right": ast2
        }


    def comparison_operation(self):
        token_type = self.current_token().type_

        result = None

        match token_type:
            case Token_type.EQUALS:
                result = "="

            case Token_type.HASH:
                result = "#" # <-- !=

            case Token_type.LESS_THAN:
                result = "<"

            case Token_type.LESS_OR_EQUAL_THAN:
                result = "<="

            case Token_type.GREATER_THAN:
                result = ">"

            case Token_type.GREATER_OR_EQUAL_THAN:
                result = ">="

            case _:
                self.syntax_error(f"Unknown comparison operation.")

        self.position += 1
        return result


    def expression(self) -> dict:

        expression_ast = self.term()

        while self.current_token().symbol in  ["+", "-"]:
            operation = self.current_token().symbol
            self.position += 1

            expression_ast = {"binary_operation":{
                "operation": operation,
                "left": expression_ast,
                "right": self.term()
                }
            }

        return expression_ast


    def term(self):
        term_ast = self.factor()

        while self.current_token().symbol in  ["*", "/"]:
            operation = self.current_token().symbol
            self.position += 1

            term_ast = {"binary_operation": {
                "operation": operation,
                "left": term_ast,
                "right": self.factor()
                }
            }

        return term_ast


    def factor(self):
        current_token = self.current_token()

        if current_token.type_ == Token_type.IDENTIFIER:
            self.check_if_current_identifier_name_is_declared()
            self.position += 1
            return {"identifier": current_token.value}

        if current_token.type_ == Token_type.NUMBER:
            self.position += 1
            return {"number": current_token.value}

        if current_token.symbol in ["+", "-"]:
            unary_operation = current_token.symbol

            self.position += 1

            ast = self.factor()
            return {"unary_operation":{"operation":unary_operation,"left":ast}}

        if current_token.symbol == "(":
            self.position += 1

            ast = self.expression()

            self.match(Token_type.RIGHT_PARENTHESIS)

            return {"expression": ast}

        error_snippet = self.original_text.split("\n")[current_token.line_number-1]
        error_position = current_token.position_number-1

        raise Invalid_syntax(f'\n\t{error_snippet}\n'
                             #f'\t{error_position * " "}^\n'
                             f'Line {current_token.line_number}: Unexpected token, {current_token}\n')

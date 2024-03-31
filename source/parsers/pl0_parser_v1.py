from parser import Parser
from token_type import Token_type
from exceptions import Invalid_syntax


class Pl0_parser_v1(Parser):

    def parse(self):
        ast = self.program()
        self.match(Token_type.EOF)
        return ast


    def program(self):
        program_ast = self.block()
        self.match(Token_type.DOT)

        return {"program": program_ast}


    def block(self):
        current_token = self.check()
        current_position = self.position

        block_ast = {}

        #Contsants declaration
        try:
            if current_token.type_ == Token_type.KEYWORD and current_token.value.lower() == "const":
                self.position += 1

                constant_declarations_list = []

                identifier_name = self.match(Token_type.IDENTIFIER).value
                self.match(Token_type.EQUALS)
                number_value = self.match(Token_type.NUMBER).value

                constant_declarations_list.append({"left": {"identifier": identifier_name},
                                                   "right": {"number": number_value}})

                while self.check().type_ == Token_type.COMMA:
                    self.position += 1
                    identifier_name = self.match(Token_type.IDENTIFIER).value
                    self.match(Token_type.EQUALS)
                    number_value = self.match(Token_type.NUMBER).value

                    constant_declarations_list.append({"left": {"identifier": identifier_name},
                                                       "right": {"number": number_value}})

                self.match(Token_type.SEMICOLON)

                block_ast["constant_declarations"] = constant_declarations_list
        except Invalid_syntax:
            self.position = current_position

        statement_ast = self.statement()

        block_ast["statement"] = statement_ast

        return {"block": block_ast}


    def statement(self):
        current_token = self.check()

        if current_token.type_ == Token_type.IDENTIFIER:
            identifier_name = self.match(Token_type.IDENTIFIER).value
            self.match(Token_type.ASSIGNMENT)
            statement_ast = self.expression()

            return {"assignment": {"left": {"identifier": identifier_name}, "right": statement_ast}}

        return None


    def expression(self) -> dict:

        expression_ast = self.term()

        while self.check().symbol in  ["+", "-"]:
            operation = self.check().symbol
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

        while self.check().symbol in  ["*", "/"]:
            operation = self.check().symbol
            self.position += 1

            term_ast = {"binary_operation": {
                "operation": operation,
                "left": term_ast,
                "right": self.factor()
                }
            }

        return term_ast


    def factor(self):
        current_token = self.check()

        if current_token.type_ == Token_type.IDENTIFIER:
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

            return ast

        error_snippet = self.original_text.split("\n")[current_token.line_number-1]
        error_position = current_token.position_number-1

        raise Invalid_syntax(f'\n\t{error_snippet}\n'
                             #f'\t{error_position * " "}^\n'
                             f'Line {current_token.line_number}: Unexpected token, {current_token}\n')

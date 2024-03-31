from _token import Token
from token_type import Token_type
from exceptions import Invalid_syntax


class Parser:

    def __init__(self, tokens: list[Token], original_text: str):
        self.tokens = tokens
        self.original_text = original_text
        self.position = 0


    def check(self) -> Token:
        current_token = self.tokens[self.position]
        return current_token


    def match(self, token_type: Token_type) -> Token | Invalid_syntax:
        current_token = self.check()

        if current_token.type_ == token_type:
            self.position += 1
            return current_token

        error_snippet = self.original_text.split("\n")[current_token.line_number - 1]
        #error_position = current_token.position_number-1

        raise Invalid_syntax(
            f'\n\t{error_snippet}\n'
            #f'\t{error_position * " "}^\n'
            f"Line {current_token.line_number}: Expected {token_type}, but got {current_token.type_}.\n"
        )

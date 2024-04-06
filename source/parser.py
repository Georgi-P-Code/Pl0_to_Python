from _token import Token
from token_type import Token_type
from exceptions import Invalid_syntax


class Parser:

    def __init__(self, tokens: list[Token], original_text: str):
        self.tokens = tokens
        self.original_text = original_text
        self.position = 0


    def current_token(self):
        try:
            return self.tokens[self.position]
        except IndexError:
            return None


    def check_token(self, token_type: Token_type, token_value=None, case_sensitive=False):

        current_token = self.current_token()

        if not case_sensitive and token_value:
            assert type(token_value) == str, \
                f"Case sensitive option turned on for non string value ({token_value}) (token_type:{token_type})"

        if current_token.type_ != token_type:
            return None

        if token_value is not None:
            if token_value != (current_token.value if case_sensitive else current_token.value.lower()):
                return None

        return current_token


    def match(self, expected_token_type: Token_type, expected_token_value=None, case_sensitive=False) -> Token | Invalid_syntax:

        current_token = self.current_token()

        if not case_sensitive and expected_token_value:
            assert type(expected_token_value) == str, \
                f"Case sensitive option turned on for non string value ({expected_token_value}) (token_type:{expected_token_type})"

        if current_token.type_ != expected_token_type:
            if_expected_token_value = f' ({expected_token_value})' if expected_token_value is not None else ""
            if_token_value = f' ({current_token.value})' if current_token.value is not None else ""

            self.syntax_error(
                f'Expected {expected_token_type}{if_expected_token_value}'
                f', but got {current_token.type_}{if_token_value}'
            )

        if expected_token_value is not None:
            if expected_token_value != (current_token.value if case_sensitive else current_token.value.lower()):
                self.syntax_error(f'Expected token value {expected_token_value}, but got {current_token.value}')

        self.position += 1
        return current_token


    def syntax_error(self, message: str):
        current_token = self.current_token()
        error_snippet = self.original_text.split("\n")[current_token.line_number - 1]

        raise Invalid_syntax(
            f'\n\t{error_snippet}\n'
            f"Line {current_token.line_number}: {message}\n"
            f"In position {self.position} for {current_token}"
        )

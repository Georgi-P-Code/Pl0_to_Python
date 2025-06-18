from _token import Token
from token_type import Token_type
from exceptions import Invalid_syntax, Semantic_analysis_error
from scope import Scope


class Parser:

    def __init__(self, tokens: list[Token], original_text: str):
        self.tokens = tokens
        self.original_text = original_text
        self.position = 0
        self.root_scope = None
        self.current_scope = None


    def get_token(self, offset: int=0):
        try:
            return self.tokens[self.position + offset]
        except IndexError:
            return None


    def current_token(self):
        return self.get_token()


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
                self.syntax_error(f'Expected token value "{expected_token_value}", but got "{current_token.value}"')

        self.position += 1
        return current_token


    def new_scope(self):
        if self.current_scope is None:
            self.root_scope = Scope(name="global")
            self.current_scope = self.root_scope
        else:
            procedure_name = self.get_token(offset=-2).value
            new_scope_instance = Scope(parent=self.current_scope, name=procedure_name)
            self.current_scope.add_scope(new_scope_instance)
            self.current_scope = new_scope_instance


    def exit_scope(self):
        if self.current_scope is None:
            raise Exception("Exited out of scope, but weren't in one")

        self.current_scope = self.current_scope.parent


    def add_identifier_to_current_scope(self, identifier_name: str, identifier_type):
        if self.current_scope is None:
            raise Exception("Tried to add identifier to scope, but weren't in one")

        existing_identifier_type = self.current_scope.identifiers.get(identifier_name)

        if existing_identifier_type == "procedure" and identifier_type == "procedure":
            #Това позволява да се редефинират процедури
            return

        if existing_identifier_type:
            self.semantic_analysis_error(
                f'Attempt to declare {identifier_type} with name "{identifier_name}"'
                f' already taken by a {existing_identifier_type}.'
            )

        self.current_scope.add_identifier(identifier_name, identifier_type)


    def check_if_current_identifier_name_is_declared(self):
        if self.current_scope is None:
            raise Exception("Tried to add identifier to scope, but weren't in one")

        if not self.check_token(Token_type.IDENTIFIER):
            raise Exception("Current token in not an identifier.")

        identifier_name = self.current_token().value

        if not self.current_scope.identifiers.get(identifier_name): #Is the identifier declared in the current scope?
            self.check_if_current_identifier_name_is_declared_in_outer_scope(identifier_name, self.current_scope)


    def check_if_current_identifier_name_is_declared_in_outer_scope(self, identifier_name: str, scope):

        current_scope = scope.parent

        if current_scope is None:
            self.semantic_analysis_error(f'Attempt to use identifier "{identifier_name}" without declaring it first.')

        if not scope.parent.identifiers.get(identifier_name): #Is the identifier declared in the current scope?
            self.check_if_current_identifier_name_is_declared_in_outer_scope(identifier_name, current_scope)


    def check_if_trying_to_change_a_constant(self, identifier_name: str):
        identifier_type = self.current_scope.identifiers.get(identifier_name)

        if identifier_type is None: # The constant is not in the current scope.
            self.check_if_trying_to_change_a_constant_from_outer_scope(identifier_name, self.current_scope)
            return

        if identifier_type == "constant":
            self.semantic_analysis_error(f'Attempt to change a constant "{identifier_name}"')


    def check_if_trying_to_change_a_constant_from_outer_scope(self, identifier_name, scope):
        current_scope = scope.parent

        identifier_type = current_scope.identifiers.get(identifier_name)

        if identifier_type is None: # The constant is not in the current scope.
            self.check_if_trying_to_change_a_constant_from_outer_scope(identifier_name, current_scope)
            return

        if identifier_type == "constant":
            self.semantic_analysis_error(f'Attempt to change a constant "{identifier_name}"')


    def error(self, exception_type, message: str):
        current_token = self.current_token()
        error_snippet = self.original_text.split("\n")[current_token.line_number - 1]

        raise exception_type(
            f'\n\t{error_snippet}\n'
            f"Line {current_token.line_number}: {message}\n"
            #f"In position {self.position} for <{current_token}>"
        )


    def syntax_error(self, message: str):
        self.error(Invalid_syntax, message)


    def semantic_analysis_error(self, message: str):
        self.error(Semantic_analysis_error, message)

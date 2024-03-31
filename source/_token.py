from typing import Any

from token_type import Token_type


class Token:

    def __init__(self, type_: Token_type, value: Any = None, line_number: int = -1, position_number: int = -1):
        self.type_ = type_
        self.value = value

        self.line_number = line_number
        self.position_number = position_number

        self.symbol: str = self.type_.value


    def __repr__(self) -> str:

        if self.value is None:
            return f'{self.type_.name}'

        else:
            if self.type_ == Token_type.STRING:
                return f'{self.type_.name} = "{self.value}"'
            else:
                return f'{self.type_.name} = {self.value}'

from enum import Enum


class Token_type(Enum):
    DOT = "."
    IDENTIFIER = "identifier"
    NUMBER = "number"
    EQUALS = "="
    COMMA = ","
    SEMICOLON = ";"
    ASSIGNMENT = ":="
    QUESTION_MARK = "?"
    EXCLAMATION = "!"
    HASH = "#"
    LESS_THAN = "<"
    LESS_OR_EQUAL_THAN = "<="
    GREATER_THAN = ">"
    GREATER_OR_EQUAL_THAN = ">="
    PLUS = "+"
    MINUS = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    LEFT_PARENTHESIS = "("
    RIGHT_PARENTHESIS = ")"
    KEYWORD = "keyword"
    SPACE = " "
    NEW_LINE = "\\n"
    TAB = "\\t"
    EOF = "end of file"


    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return self.value == other.value

import re

from _token import Token
from keywords import keywords
from token_type import Token_type


class Tokenizer:

    def __init__(self, text: str, ignore_space: bool = True, ignore_new_line: bool = False):
        self.text = text
        self.ignore_space = ignore_space
        self.ignore_new_line = ignore_new_line

        self.tokenize()


    def tokenize(self):
        if self.text == "":
            return [Token(Token_type.EOF, line_number= 1, position_number= 0)]

        self.position = 0
        self.position_in_current_line = 0
        self.tokens = []
        self.line_number = 1

        while self.position < len(self.text):
            char = self.text[self.position]

            if char.isdigit():
                number = self.parse_number()
                if number.isdecimal():
                    self.tokens.append(Token(Token_type.NUMBER, int(number)))
                else:
                    self.tokens.append(Token(Token_type.NUMBER, float(number)))

            elif char == "+":
                self.tokens.append(Token(Token_type.PLUS))

            elif char == "-":
                self.tokens.append(Token(Token_type.MINUS))

            elif char == "*":
                self.tokens.append(Token(Token_type.MULTIPLICATION))

            elif char == "/":
                self.tokens.append(Token(Token_type.DIVISION))

            elif char == " ":
                if not self.ignore_space:
                    self.tokens.append(Token(Token_type.SPACE))

            elif char == "(":
                self.tokens.append(Token(Token_type.LEFT_PARENTHESIS))

            elif char == ")":
                self.tokens.append(Token(Token_type.RIGHT_PARENTHESIS))

            elif char == "=":
                self.tokens.append(Token(Token_type.EQUALS))

            elif char == ",":
                self.tokens.append(Token(Token_type.COMMA))

            elif char == ".":
                self.tokens.append(Token(Token_type.DOT))

            elif char == "?":
                self.tokens.append(Token(Token_type.QUESTION_MARK))

            elif char == "<":
                next_char = self.get_next_char()

                if next_char == "=":
                    self.tokens.append(Token(Token_type.LESS_OR_EQUAL_THAN))
                else:
                    self.tokens.append(Token(Token_type.LESS_THAN))

            elif char == ">":
                next_char = self.get_next_char()

                if next_char == "=":
                    self.tokens.append(Token(Token_type.GREATER_OR_EQUAL_THAN))
                else:
                    self.tokens.append(Token(Token_type.GREATER_THAN))

            elif char == ";":
                self.tokens.append(Token(Token_type.SEMICOLON))

            elif char == ":" and self.get_next_char() == "=":
                self.tokens.append(Token(Token_type.ASSIGNMENT))
                self.position += 1

            elif char == "!":
                self.tokens.append(Token(Token_type.EXCLAMATION))

            elif char == "#":
                self.tokens.append(Token(Token_type.HASH))

            elif char == "\t":
                if not self.ignore_space:
                    self.tokens.append(Token(Token_type.TAB))

            elif char == "\n":
                if not self.ignore_new_line:
                    self.tokens.append(Token(Token_type.NEW_LINE))
                self.line_number += 1

            elif char.isalpha() or char == "_":
                identifier = self.parse_identifier()
                if identifier.lower() in keywords:
                    self.tokens.append(Token(Token_type.KEYWORD, identifier))
                else:
                    self.tokens.append(Token(Token_type.IDENTIFIER, identifier))

            else:
                raise Exception(f"Unknown character {char} at line {self.line_number}")

            if char == "\n":
                if not self.ignore_new_line:
                    self.tokens[-1].line_number = self.line_number-1

            elif char == " ":
                if not self.ignore_space:
                    self.tokens[-1].line_number = self.line_number

            else:
                if self.tokens[-1].line_number == -1:
                    self.tokens[-1].line_number = self.line_number

            self.position += 1

        self.tokens.append(Token(Token_type.EOF, line_number=self.line_number))

        return self.tokens


    def get_char(self):
        try:
            return self.text[self.position]
        except IndexError:
            return None


    def get_next_char(self):
        try:
            return self.text[self.position+1]
        except IndexError:
            return None


    def parse_number(self):
        result = re.match("[0-9]+[.][0-9]+", self.text[self.position:])

        if result is not None:
            self.position += result.end()-1
            return result.group()

        result = re.match("[0-9]+", self.text[self.position:])

        if result is not None:
            self.position += result.end()-1
            return result.group()
        else:
            raise Exception(f"Error while parsing a number at line {self.line_number} for {result}")


    def parse_identifier(self):
        result = re.match("[a-zA-Z_][0-9a-zA-Z_]*", self.text[self.position:])

        if result is not None:
            self.position += result.end()-1
            return result.group()
        else:
            raise Exception(f"Error while parsing an identifier at line {self.line_number} for {result}")


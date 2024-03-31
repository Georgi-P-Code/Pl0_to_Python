from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator
from exceptions import Invalid_syntax

def main():

    while True:
        input_ = input(">")

        if input_ == "exit":
            break

        if input_ == "clear":
            print("\n" * 20)
            continue

        tokens = Tokenizer(input_).tokenize()
        print("tokens:", tokens)
        try:
            ast = Pl0_parser_v1(tokens, input_).parse()
            python_file = Translator(ast).translate()
            print("ast:", ast)
            print("python_file:", python_file)
        except Invalid_syntax as syntax_error:
            print("Error:", syntax_error)
            continue


if __name__ == "__main__":
    main()

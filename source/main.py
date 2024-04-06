import json
from os import path, mkdir

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from exceptions import Invalid_syntax


def main():

    path_to_file = "../programs/example_2.pl0"
    file_name = path_to_file[path_to_file.rfind("/")+1:path_to_file.rfind(".")]

    input_text = load_program(path_to_file)

    tokens, ast, output_text = execute(input_text, file_name, save_ast=True)

    print_execution_results(input_text, tokens, ast, output_text)

    with open(f"../output/{file_name}.py", "w") as f:
        f.write(output_text)


    # while True:
    #     input_text = input(">")
    #
    #     if input_text == "exit":
    #         break
    #
    #     if input_text == "clear":
    #         print("\n" * 20)
    #         continue
    #
    #     try:
    #         tokens, ast, output_text = execute(input_text)
    #     except Invalid_syntax as syntax_error:
    #         print("Syntax error:", syntax_error)
    #         continue
    #
    #     print_execution_results(input_text, tokens, ast, output_text)


def execute(input_text: str, file_name: str="untitled", ignore_new_line=True, save_ast=False):
    tokens = Tokenizer(input_text, ignore_new_line=ignore_new_line).tokenize()

    #try:
    ast = Pl0_parser_v1(tokens, input_text).parse()
    # except Invalid_syntax as err:
    #     return tokens, err, ""

    if save_ast:
        path_to_file_dir = f"../debugging/{file_name}"

        if path.exists(path_to_file_dir):
            assert path.isdir(path_to_file_dir)
        else:
            mkdir(path_to_file_dir)


        with open(f"{path_to_file_dir}/{file_name}_ast.json", "w") as f:
            f.write(json.dumps(ast, indent=2))

    output_text = Translator(ast).translate()

    return tokens, ast, output_text


def print_execution_results(input_: str, tokens, ast, output_text: str):
    print("-----------------------")
    print(input_)
    print("-----------------------")
    print("Tokens:", tokens)
    print("-----------------------")
    print("Ast:", ast)
    print("-----------------------")
    print(output_text)
    print("-----------------------")


def load_program(program_path: str):
    #validate path TODO
    with open(program_path, "r") as f:
        return f.read()



if __name__ == "__main__":
    main()

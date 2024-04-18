import json
from os import path, mkdir

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from utilities.ast_visualizer import Ast_visualizer
from utilities.tokens_visualizer import Tokens_visualizer

from exceptions import Invalid_syntax


def main():

    name = "all_grammar_use"

    run_file(f"{name}.pl0", debugging=True)

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
    #         tokensz, ast, output_text = execute(input_text)
    #     except Invalid_syntax as syntax_error:
    #         print("Syntax error:", syntax_error)
    #         continue
    #
    #     print_execution_results(input_text, tokensz, ast, output_text)


def run_file(file_name_with_extension: str, debugging=False):
    path_to_file = f"../input/{file_name_with_extension}"

    if not path.exists(path_to_file):
        raise Exception(f'There is no file with name {file_name_with_extension} in the input directory.')

    file_name = path_to_file[path_to_file.rfind("/")+1:path_to_file.rfind(".")]

    input_text = read_file(path_to_file)

    print("-----------------------")
    print(input_text)

    tokens = Tokenizer(input_text, ignore_new_line=True).tokenize()

    tokens_visualization = Tokens_visualizer(tokens).visualize()

    print("-----------------------")
    print("Tokens:", tokens_visualization)

    ast = Pl0_parser_v1(tokens, input_text).parse()

    str_repr = Ast_visualizer(ast).visualize()

    print("-----------------------")
    print(f"Ast:\n{str_repr}")

    if debugging:
        path_to_file_dir = f"../debugging/{file_name}"

        if path.exists(path_to_file_dir):
            assert path.isdir(path_to_file_dir)
        else:
            mkdir(path_to_file_dir)

        with open(f"{path_to_file_dir}/{file_name}_ast.json", "w") as f:
            f.write(json.dumps(ast, indent=2))

    output_text = Translator(ast).translate()

    print("-----------------------")
    print(output_text)
    print("-----------------------")

    with open(f"../output/{file_name}.py", "w") as f:
        f.write(output_text)


def execute(input_text: str, file_name: str="untitled", ignore_new_line=True, save_ast=False):
    tokens = Tokenizer(input_text, ignore_new_line=ignore_new_line).tokenize()

    #try:
    ast = Pl0_parser_v1(tokens, input_text).parse()
    # except Invalid_syntax as err:
    #     return tokensz, err, ""

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
    # comp = compile(output_text, "<string>","eval")
    # eval(comp)

def read_file(program_path: str):
    #validate path TODO
    with open(program_path, "r") as f:
        return f.read()



if __name__ == "__main__":
    main()

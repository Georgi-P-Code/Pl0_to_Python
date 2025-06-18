import json
from os import path, mkdir
import subprocess

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from utilities.ast_visualizer import Ast_visualizer
from utilities.tokens_visualizer import Tokens_visualizer


def run_file(path_to_file: str, debugging=False):

    if not path.exists(path_to_file):
        error_message = f'Error: "{path_to_file}" is not a valid file path.'
        print(error_message)
        return Exception(error_message)

    file_name = path.split(path_to_file)[-1]

    input_text = read_file(path_to_file)

    if debugging:
        print("------ Input Program ------")
        print(input_text)
        print("---------------------------")

    tokens = Tokenizer(input_text, ignore_new_line=True).tokenize()

    if debugging:
        tokens_visualization = Tokens_visualizer(tokens).visualize()

        print("--------- Tokens ----------")
        print(f"{tokens_visualization}")
        print("---------------------------")

    parser = Pl0_parser_v1(tokens, input_text)
    ast = parser.parse()
    scope_information = parser.root_scope

    if debugging:
        ast_visualization = Ast_visualizer(ast).visualize()
        print("---------- AST ------------")
        print(f"{ast_visualization}")
        print("---------------------------")

        if not path.exists("../debugging/"):
            mkdir("../debugging/")

        path_to_file_dir = f"../debugging/{file_name}"

        if path.exists(path_to_file_dir):
            assert path.isdir(path_to_file_dir)
        else:
            mkdir(path_to_file_dir)

        with open(f"{path_to_file_dir}/{file_name}_ast.json", "w") as f:
            f.write(json.dumps(ast, indent=2))

    output_text = Translator(ast, scope_information).translate()

    if debugging:
        print("- Generated Python Program -")
        print(output_text)
        print("----------------------------")

    if not path.exists("../output/"):
        mkdir("../output/")

    with open(f"../output/{file_name}.py", "w") as f:
        f.write(output_text)

    print("------ Python Output -------")

    subprocess.run(f"python ../output/{file_name}.py", shell=True)

    print("----------------------------")


def read_file(program_path: str):
    with open(program_path, "r", encoding="utf-8") as f:
        return f.read()
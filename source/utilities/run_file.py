import json
from os import path, mkdir
import subprocess

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from utilities.ast_visualizer import Ast_visualizer
from utilities.tokens_visualizer import Tokens_visualizer


def run_file(file_name_with_extension: str, debugging=False):
    path_to_file = f"../input/{file_name_with_extension}"

    if not path.exists(path_to_file):
        raise Exception(f'There is no file with name {file_name_with_extension} in the input directory.')

    file_name = path_to_file[path_to_file.rfind("/")+1:path_to_file.rfind(".")]

    input_text = read_file(path_to_file)

    print("------ Input Program ------")
    print(input_text)
    print("---------------------------")

    tokens = Tokenizer(input_text, ignore_new_line=True).tokenize()

    tokens_visualization = Tokens_visualizer(tokens).visualize()

    print("--------- Tokens ----------")
    print(f"{tokens_visualization}")
    print("---------------------------")

    parser = Pl0_parser_v1(tokens, input_text)
    ast = parser.parse()
    scope_information = parser.root_scope
    ast_visualization = Ast_visualizer(ast).visualize()

    print("---------- AST ------------")
    print(f"{ast_visualization}")
    print("---------------------------")

    if debugging:
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
    with open(program_path, "r") as f:
        return f.read()
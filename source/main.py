import json
from os import path, mkdir

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from utilities.ast_visualizer import Ast_visualizer
from utilities.tokens_visualizer import Tokens_visualizer


def main():
    run_file(f"fibonacci.pl0", debugging=True)


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

    ast = Pl0_parser_v1(tokens, input_text).parse()

    str_repr = Ast_visualizer(ast).visualize()

    print("---------- AST ------------")
    print(f"{str_repr}")
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

    output_text = Translator(ast).translate()

    print("- Generated Python Program -")
    print(output_text)
    print("----------------------------")

    if not path.exists("../output/"):
        mkdir("../output/")

    with open(f"../output/{file_name}.py", "w") as f:
        f.write(output_text)

    print("------ Python Output -------")

    try:
        exec(output_text)
    except Exception as err:
        print(f'Error: {err}')

    print("----------------------------")


def read_file(program_path: str):
    with open(program_path, "r") as f:
        return f.read()


if __name__ == "__main__":
    main()

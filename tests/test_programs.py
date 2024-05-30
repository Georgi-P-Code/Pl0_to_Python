import os
import subprocess
import pytest

from exceptions import Invalid_syntax, Semantic_analysis_error

from tokenizer import Tokenizer
from parsers import Pl0_parser_v1
from ast_to_python import Translator

from utilities.tokens_visualizer import Tokens_visualizer
from utilities.ast_visualizer import Ast_visualizer


def run_file(file_name: str):

    file_path = f"./test_programs/{file_name}"

    if not os.path.exists(file_path):
        raise Exception(f"No file with name {file_name}")

    with open(file_path, "r") as f:
        input_text = f.read()

    tokens = Tokenizer(input_text, ignore_new_line=True).tokenize()
    tokens_visualization = Tokens_visualizer(tokens).visualize()

    parser = Pl0_parser_v1(tokens, input_text)
    ast = parser.parse()
    scope_information = parser.root_scope
    ast_visualization = Ast_visualizer(ast).visualize()

    output_text = Translator(ast, scope_information).translate()

    if not os.path.exists("testing_temp/"):
        os.mkdir("testing_temp/")

    with open(f"testing_temp/{file_name}.py", "w") as f:
        f.write(output_text)

    python_process = subprocess.run(f"python testing_temp/{file_name}.py", capture_output=True)
    python_output = python_process.stdout.decode("utf-8").replace("\r\n", "\n")

    return "\n---\n".join([str(tokens), tokens_visualization, str(ast), ast_visualization, output_text, python_output])


def get_expected_output(file_name: str):
    file_path = f"./test_programs_expected_output/{file_name}"

    if not os.path.exists(file_path):
        raise Exception(f"No file with name {file_name}")

    with open(file_path, "r", encoding="utf-8") as f:
        expected_output_text = f.read()

    return expected_output_text


def generate_expected_output(program_name: str):
    results = run_file(f"{program_name}.pl0")

    file_path = f"./test_programs_expected_output/{program_name}_expected_output.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(results)


def full_test(program_name: str):
    results = run_file(f"{program_name}.pl0")
    expected_output = get_expected_output(f"{program_name}_expected_output.txt")

    assert results == expected_output


def show(program_name: str):
    print(run_file(f"{program_name}.pl0"))


def test_empty_file():
    with pytest.raises(Invalid_syntax):
        full_test("empty_file")


def test_empty_program():
    full_test("empty_program")


def test_variable_definition():
    full_test("variable_declaration")


def test_variable_use_before_declaration():
    expected_error_text = 'Attempt to use identifier "a" without declaring it first.'
    with pytest.raises(Semantic_analysis_error, match=expected_error_text):
        full_test("variable_use_before_declaration")


def test_variables_definition():
    full_test("variables_declaration")


def test_constant_declaration():
    full_test("constant_declaration")


def test_constants_declaration():
    full_test("constants_declaration")


def test_constant_change():
    expected_error_text = '\n\t    max := 200;\n' \
                          'Line 3: Attempt to change a constant "max"\n'
    with pytest.raises(Semantic_analysis_error, match=expected_error_text):
        full_test("constant_change")


def test_setting_outer_scope_declared_variable():
    full_test("setting_outer_scope_declared_variable")


def test_same_variable_name_in_different_scopes():
    full_test("same_variable_name_in_different_scopes")


def test_global_variable_in_procedure():
    expected_error_text = '\n\t    !b\n' \
                          'Line 26: Attempt to use identifier "b" without declaring it first.\n'
    with pytest.raises(Semantic_analysis_error, match=expected_error_text):
        full_test("global_variable_in_procedure") # Трябва даде грешка че променливата b не е декларина.


def test_variable_and_constant_with_the_same_name():
    expected_error_text = '\n\tvar max;\n' \
                          'Line 2: Attempt to declare variable with name "max" already taken by a constant.\n'
    with pytest.raises(Semantic_analysis_error, match=expected_error_text):
        full_test("variable_and_constant_with_the_same_name")


def test_counter():
    full_test("counter")


def test_prime_numbers():
    full_test("prime_numbers")
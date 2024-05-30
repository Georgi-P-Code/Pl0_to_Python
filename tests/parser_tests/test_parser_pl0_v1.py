from source.tokenizer import Tokenizer
from source.parsers import Pl0_parser_v1

def test_basic_program():
    input_ = """var _exe_; _exe_ := 1/-1 ."""

    target = "{'program': {'block': \
{'variable_declarations': [{'identifier': '_exe_'}], \
'statement': {'assignment': {'left': {'identifier': '_exe_'}, \
'right': {'binary_operation': {'operation': '/', 'left': {'number': 1}, \
'right': {'unary_operation': {'operation': '-', 'left': {'number': 1}}}}}}}}}}"

    tokens = Tokenizer(input_, ignore_new_line=True).tokenize()
    ast = Pl0_parser_v1(tokens, input_).parse()

    assert  target == str(ast)
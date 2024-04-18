from source.tokenizer import Tokenizer

def test_assignment():

    input_ = "const asd := 11;"

    tokens = Tokenizer(input_).tokenize()
    assert str(tokens) == "[KEYWORD = const, IDENTIFIER = asd, ASSIGNMENT, NUMBER = 11, SEMICOLON, EOF]"



# TEST CASE FAIL !!!    asd = """\
#
# """
from _token import Token


class Tokens_visualizer:

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.line_number = 0


    def visualize(self):
        out = ""

        for token in self.tokens:

            if token.line_number > self.line_number:
                self.line_number = token.line_number
                if token.line_number == 1:
                    out += f'{self.line_number}: '
                else:
                    out += f"\n{self.line_number}: "

            out += f'<{token}> '

        return out


if __name__ == '__main__':
    from tokenizer import Tokenizer

    asd = """\
Var i, a, b, c, max;

begin

    a := 1;

    if odd a + 1 + 3 then
        a := 2

    a := 0;
    b := 1;

    !a;
    !b;

    while i < max do
    begin
        c := a + b;
        !c;
        a := b;
        b := c;
        i := i + 1
    end
end.
"""

    tokens = Tokenizer(asd, ignore_new_line=True).tokenize()

    tokens_visualization = Tokens_visualizer(tokens).visualize()

    print(tokens_visualization)
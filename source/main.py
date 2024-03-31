from tokenizer import Tokenizer


def main():

    while True:
        input_ = input(">")

        if input_ == "exit":
            break

        if input_ == "clear":
            print("\n" * 20)
            continue

        # try:
        tokens = Tokenizer(input_).tokenize()
        print("tokens:", tokens)
        # except Exception as result:
        #     print(result)
        #     continue


if __name__ == "__main__":
    main()

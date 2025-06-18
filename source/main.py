import argparse

from utilities.run_file import run_file


def main(input_file: str, debug_flag):
    run_file(input_file, debugging=debug_flag)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog="pl0_to_python")
    arg_parser.add_argument("input_file", help="path to input file")
    arg_parser.add_argument("-d", "--debug", help="debugging option", action='store_true')
    args = arg_parser.parse_args()

    main(args.input_file, args.debug)

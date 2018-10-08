#!/Users/sanchez/Projects/py/Anaconda/anaconda/bin/python

import os
import sys
import argparse
from lexer import tokens_groups, tokenize_naked, tokenize_named
import parser

argparser = argparse.ArgumentParser(description='Lexer parsing.')
argparser.add_argument("--file", "-f", dest="file", type=str,
                    help="file to parse")


if __name__ == "__main__":

    args = argparser.parse_args()
    file_to_lex = os.path.join(sys.path[0], args.file)

    with open(file_to_lex, "r") as f:
        content = f.read()
        print ("Lexing: \n{}".format(content))

        tokenized = tokenize_naked(content)
        print ("Tokenised: \n{}".format(tokenized))

        tokenized_fully = tokenize_named(tokenized)
        print ("Tokenised: \n{}".format(tokenized_fully))

        ast = parser.parse_program_string(content)
        print ("AST: \n{}".format(ast))
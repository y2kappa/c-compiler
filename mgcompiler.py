#!/Users/sanchez/Projects/py/Anaconda/anaconda/bin/python

import os
import sys
import argparse
import subprocess
from lexer import tokens_groups, tokenize_naked, tokenize_named
import parser
import generator

argparser = argparse.ArgumentParser(description='Lexer parsing.')
argparser.add_argument(dest="file", type=str,
                    help="file to compile")


if __name__ == "__main__":

    args = argparser.parse_args()
    file_to_lex = os.path.join(sys.path[0], args.file)

    if file_to_lex[-2:] != ".c":
        print ("Your file is not a .c file")
        exit(1)

    with open(file_to_lex, "r") as f:
        content = f.read()
        print ("Lexing: \n{}".format(content))

        tokenized = tokenize_naked(content)
        print ("Tokenised: \n{}".format(tokenized))

        tokenized_fully = tokenize_named(tokenized)
        print ("Tokenised: \n{}".format(tokenized_fully))

        ast = parser.parse_program_string(content)
        print ("AST: \n{}".format(ast))

        if ast is None:
            print ("Error parsing")
            exit(1)

        assembly = generator.generate(ast)
        print ("Assembly: \n{}".format(assembly))

        file_to_write = file_to_lex[:-2] + ".s"
        with open(file_to_write, 'w') as fw:
            fw.write(assembly)


        p = subprocess.Popen(["gcc", file_to_write, "-m32", "-O3", "-fno-asynchronous-unwind-tables", "-o", file_to_write[:-2]])


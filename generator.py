#!/Users/sanchez/Projects/py/Anaconda/anaconda/bin/python

import parser

def generate(ast):
    assembly = ".globl _{}\n".format(ast.function_name)
    assembly += "_{}:\n".format(ast.function_name)

    return_value = ast.function_statement.expression.token.token
    assembly += "movl\t${}, %eax\n".format(return_value)
    assembly += "retq"

    return assembly

if __name__ == "__main__":
    text = "int main() { return 20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)

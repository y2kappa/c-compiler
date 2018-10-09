#!/Users/sanchez/Projects/py/Anaconda/anaconda/bin/python

import lexer
import parser

def generate_expression_assembly(expression):
    assembly = ""
    
    if type(expression) == parser.Constant:
        return_value = expression.token.token
        assembly += "movl\t${}, %eax\n".format(return_value)

    if type(expression) == parser.UnaryOperation:
        assembly +=  generate_expression_assembly(expression.expression)

        if expression.operator == lexer.Operator("-"):
            assembly += "neg\t%eax\n"
            
        if expression.operator == lexer.Operator("!"):
            assembly += "cmpl\t$0, %eax\n"
            assembly += "movl\t$0, %eax\n"
            assembly += "sete\t%al\n"
        
        if expression.operator == lexer.Operator("~"):
            assembly += "not\t%eax\n"

    return assembly

def generate_statement_assembly(statement):
    assembly = ""
    if type(statement) == parser.ReturnStatement:
        assembly = generate_expression_assembly(statement.expression)
        assembly += "retq" 
        
    return assembly

def generate(ast):
    assembly = ".globl _{}\n".format(ast.function_name)
    assembly += "_{}:".format(ast.function_name)

    remaining_assembly = "\n"
    remaining_assembly += generate_statement_assembly(ast.function_statement)
    remaining_assembly = remaining_assembly.replace("\n","\n\t")

    #return_value = ast.function_statement.expression
    #assembly += "movl\t${}, %eax\n".format(return_value)
    #assembly += "retq"

    assembly += remaining_assembly
    return assembly

if __name__ == "__main__":
    text = "int main() { return 20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

    text = "int main() { return !20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

    text = "int main() { return -20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

    text = "int main() { return ~20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

    text = "int main() { return !!20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

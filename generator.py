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

    if type(expression) == parser.BinaryOperation:
        
        

        if expression.operator == lexer.Operator("+") or \
            expression.operator == lexer.Operator("*"):

            first_operand = expression.lhs
            second_operand = expression.rhs

        elif expression.operator == lexer.Operator("-") or \
            expression.operator == lexer.Operator("/"):

            first_operand = expression.rhs
            second_operand = expression.lhs
            
        assembly += generate_expression_assembly(first_operand)
        assembly += "pushl\t%eax\n"

        assembly += generate_expression_assembly(second_operand)
        assembly += "popl\t%ecx\n" 
        
        # at this point:

        # if + or * 
        # a -> ecx
        # b -> eax

        # else
        # a -> eax
        # b -> ecx

        if expression.operator == lexer.Operator("+"):
            assembly += "addl\t%ecx, %eax\n" # sum and store in eax
        elif expression.operator == lexer.Operator("*"):
            assembly += "imul\t%ecx, %eax\n" # multiply and store in eax

        elif expression.operator == lexer.Operator("-"):
            assembly += "subl\t%ecx, %eax\n" # substract eax - ecx and store in eax
        elif expression.operator == lexer.Operator("/"):
            # zero out edx
            assembly += "movl\t$0, %edx\n"
            assembly += "idivl\t%ecx\n"


        
    return assembly

def generate_statement_assembly(statement):
    assembly = ""
    if type(statement) == parser.ReturnStatement:
        assembly = generate_expression_assembly(statement.expression)
        assembly += "ret\n" 
        
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

    assembly += remaining_assembly + "\n"
    return assembly

if __name__ == "__main__":
    text = "int main() { return 20; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (assembly)
    print ("----")

    text = "int main() { return 20 + 15; }"
    ast = parser.parse_program_string(text)
    assembly = generate(ast)
    print (ast)
    
    print (assembly)
    print ("----")

    # text = "int main() { return !20; }"
    # ast = parser.parse_program_string(text)
    # assembly = generate(ast)
    # print (assembly)
    # print ("----")

    # text = "int main() { return -20; }"
    # ast = parser.parse_program_string(text)
    # assembly = generate(ast)
    # print (assembly)
    # print ("----")

    # text = "int main() { return ~20; }"
    # ast = parser.parse_program_string(text)
    # assembly = generate(ast)
    # print (assembly)
    # print ("----")

    # text = "int main() { return !!20; }"
    # ast = parser.parse_program_string(text)
    # assembly = generate(ast)
    # print (assembly)
    # print ("----")

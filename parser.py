import lexer
from collections import deque

class Statement:
    def __init__(self):
        pass

    def isStatement(self):
        return True
        
class ReturnStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return "return {}".format(self.expression.__repr__())

def parse_return_statement(tokens):
    tokens_backup = deque(tokens)

    token = tokens_backup.pop()
    if token != lexer.Keyword("return"):
        print ("Could not find return keyword. {} {}".format(token, tokens_backup))
        return None, tokens


    expr, tokens_backup = parse_expression(tokens_backup)

    if expr is None:
        return None, tokens
    else:
        return ReturnStatement(expr), tokens_backup

def parse_statement(tokens):
    
    # try return statement
    statement, remaining_tokens = parse_return_statement(tokens)
    if statement is None:
        print ("Could not parse statement as return statement")
    else:
        return statement, remaining_tokens

    return None, tokens

class Expression:
    
    def __init__(self):
        pass

    def isExpression(self):
        return True

class Constant(Expression):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Constant({})".format(self.token)

def parse_expression(tokens):
    # print ("Parsing expression {}".format(tokens))
    tokens_backup = deque(tokens)

    if len(tokens_backup) == 0:
        print ("There are no tokens, cannot parse the expression")
        return False, tokens

    token = tokens_backup.pop()
    # print ("Extracted: {} remaining {}".format(token, tokens_backup))

    if type(token) != lexer.Number:
        print ("Expected a number, could not find it")
        return False, tokens

    number = token
    
    if len(tokens_backup) == 0:
        print ("Empty, semicolon not following")
        return False, tokens

    token = tokens_backup.pop()
    # print ("Extracted: {} remaining {}".format(token, tokens_backup))
    if token != lexer.Punctuation(';'):
        print ("Not semicolon {} != {}".format(token, lexer.Punctuation(';')))
        return False, tokens

    return Constant(number), tokens_backup

class Function:
    def __init__(self, function_return_type, function_name, function_statement):
        self.function_return_type = function_return_type
        self.function_name = function_name
        self.function_statement = function_statement

    def __repr__(self):
        return "FUNCTION {} {}: \n\tparams: ()\n\tbody:\n\t\t{} \n}}".format(
            self.function_return_type.__repr__(), 
            self.function_name.__repr__(),
            self.function_statement.__repr__())

def parse_function(tokens):
    tokens_backup = deque(tokens)

    function_return_type = None
    function_name = None
    function_statement = None


    # get return type
    token = tokens_backup.pop()
    if token != lexer.Type("int"):
        print ("Could not find return type int.\n{} vs {}".format(token, lexer.Type("int")))
        return None, tokens
    else:
        function_return_type = token

    # get name
    token = tokens_backup.pop()
    if token != lexer.Identifier("main"):
        print ("Could not find function name main.")
        return None, tokens
    else:
        function_name = token

    # get open parens, get close parens
    token = tokens_backup.pop()
    if token != lexer.Punctuation("("):
        print ("Could not find open parens.")
        return None, tokens

    token = tokens_backup.pop()
    if token != lexer.Punctuation(")"):
        print ("Could not find close parens.")
        return None, tokens

    # get open brace
    token = tokens_backup.pop()
    if token != lexer.Punctuation("{"):
        print ("Could not find open braces.")
        return None, tokens
    
    # get statement
    statement, tokens_backup = parse_statement(tokens_backup)
    if statement is None:
        print ("Could not parse function statement.")
        return None, tokens
    else:
        function_statement = statement
    
    # get close brace
    token = tokens_backup.pop()
    if token != lexer.Punctuation("}"):
        print ("Could not find close braces.")
        return None, tokens

    function = Function(function_return_type, function_name, function_statement)

    return function, tokens_backup

class Program:
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return "PROGRAM \n{}".format(self.function)

def parse_ast(named_tokens):
    function = parse_function(named_tokens)
    return function

def parse_program_string(program_string):
    program_tokens_naked = lexer.tokenize_naked(program_string)
    program_tokens_named = lexer.tokenize_named(program_tokens_naked)
    
    tokens = deque([x for x in reversed(program_tokens_named)])
    program_ast, _ = parse_ast(tokens)

    return program_ast

if __name__ == "__main__":
    program_text = "int main() { return 23; }"
    print(parse_program_string(program_text))
    

    


#!/Users/sanchez/Projects/py/Anaconda/anaconda/bin/python

import lexer
import logging
from collections import deque

logging.basicConfig(
    format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

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
        logging.error ("Could not find return keyword. {} {}".format(token, tokens_backup))
        return None, tokens

    expr, tokens_backup = parse_expression(tokens_backup)
    #logging.debug ("Extracted expression {}".format(expr))

    if len(tokens_backup) == 0:
        logging.error ("Empty, semicolon not following")
        return None, tokens

    token = tokens_backup.pop()
    if token != lexer.Punctuation(';'):
        logging.error ("Not semicolon {} != {}".format(token, lexer.Punctuation(';')))
        return None, tokens

    if expr is None:
        return None, tokens
    else:
        return ReturnStatement(expr), tokens_backup

def parse_statement(tokens):
    
    # try return statement
    statement, remaining_tokens = parse_return_statement(tokens)
    if statement is None:
        logging.error ("Could not parse statement as return statement")
    else:
        #logging.debug ("Found statement: {}".format(statement))
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

class UnaryOperation(Expression):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self):
        return "UnaryOperation({}, {})".format(self.operator, self.expression)

class BinaryOperation(Expression):
    def __init__(self, operator, lhs, rhs):
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return "BinaryOperation({}, {}, {})".format(self.operator, self.lhs, self.rhs)

class Term(Expression):
    pass

class Factor(Expression):
    pass

def parse_factor(tokens):
    #print ("Parsing factor {}".format(tokens))
    tokens_backup = deque(tokens)

    if len(tokens_backup) == 0:
        print ("There are no tokens, cannot parse the term")
        return None, tokens

    token = tokens_backup.pop()
    if token == lexer.Punctuation("("):
        expression, tokens_backup = parse_expression(tokens_backup)

        if expression is None:
            return None, tokens

        token = tokens_backup.pop()
        if token != lexer.Punctuation(")"):
            return None, tokens

        return expression, tokens_backup


    elif token == lexer.Operator("-") or \
        token == lexer.Operator("!") or \
        token == lexer.Operator("~"):

        operator = token
        inner_factor, tokens_backup = parse_factor(tokens_backup)

        if inner_factor is None:
            return None, tokens

        return UnaryOperation(operator, inner_factor), tokens_backup

    elif type(token) == lexer.Number:
        number = token
        return Constant(number), tokens_backup

    return None, tokens

def parse_term(tokens):
    #print ("Parsing term {}".format(tokens))
    tokens_backup = deque(tokens)

    if len(tokens_backup) == 0:
        print ("There are no tokens, cannot parse the term")
        return None, tokens

    # token = tokens_backup.pop()
    factor, tokens_backup = parse_factor(tokens_backup)
    if factor is None:
        return None, tokens

    next = tokens_backup[-1]
    while next == lexer.Operator("*") or next == lexer.Operator("/"):
        operator = tokens_backup.pop()
        next_factor, tokens_remaining = parse_factor(tokens_backup)
        if next_factor is None:
            return None, tokens_backup

        tokens_backup = tokens_remaining
        factor = BinaryOperation(operator, factor, next_factor)
        next = tokens_backup[-1]

    return factor, tokens_backup

def parse_expression(tokens):
    #print ("Parsing expression {}".format(tokens))
    tokens_backup = deque(tokens)

    if len(tokens_backup) == 0:
        print ("There are no tokens, cannot parse the expression")
        return None, tokens

    # token = tokens_backup.pop()
    term, tokens_backup = parse_term(tokens_backup)
    if term is None:
        return None, tokens
    else:
        pass
        #print ("Extracted term {}.".format(term))
        #print ("Remaining {}.".format(tokens_backup))

    next = tokens_backup[-1] # because it's reversed and pop takes from the end
    
    while next == lexer.Operator("+") or next == lexer.Operator("-"):
        operator = tokens_backup.pop()
        next_term, tokens_remaining = parse_term(tokens_backup)
        if next_term is None:
            return None, tokens_backup

        tokens_backup = tokens_remaining
        term = BinaryOperation(operator, term, next_term)
        next = tokens_backup[-1]

    return term, tokens_backup

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
    print (program_tokens_naked)
    program_tokens_named = lexer.tokenize_named(program_tokens_naked)
    
    tokens = deque([x for x in reversed(program_tokens_named)])
    program_ast, _ = parse_ast(tokens)

    return program_ast

if __name__ == "__main__":
    #program_text = "int main() { return 23; }"
    #print (parse_program_string(program_text))
    #print ("\n----\n")

    #program_text = "int main() { return 23 + 25; }"
    #print (parse_program_string(program_text))
    #print ("\n----\n")

    program_text = "int main() { return 1 - 2 - 3; }"
    print (parse_program_string(program_text))
    print ("\n----\n")
    

    


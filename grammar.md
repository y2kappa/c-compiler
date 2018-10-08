## Grammar (Backus-Naur Form)

<program> ::= <function>
<function> ::= "int" <id> "(" ")" "{" <statement> "}"
<statement> ::= "return" <exp> ";"
<exp> ::= <int>

## Pseudocode

program = Program(function_declaration)
function_declaration = Function(string, statement) // string is the function mame
statement = Return(exp)
exp = Constant(int)
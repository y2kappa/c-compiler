## Grammar (Backus-Naur Form)

```html
<program>       ::= <function>
<function>      ::= "int" <id> "(" ")" "{" <statement> "}"
<statement>     ::= "return" <exp> ";"
<exp>           ::= <term> { ("+" | "-") <term> }
<term>          ::= <factor> { ("*" | "/") <factor> }
<factor>        ::= "(" <exp> ")" | <unary_op> <factor> | <int>

```


## Pseudocode

```ocaml
program = Program(function_declaration)
function_declaration = Function(string, statement) (* string is the function mame *)
statement = Return(exp)
exp = BinOp(binary_operator, exp, exp)
    | UnOp(operator, exp) 
    | Constant(int)
    
```
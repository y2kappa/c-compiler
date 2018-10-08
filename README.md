# Writing a C Compiler

## What I will learn

- ASTs, linters, static analyzers, metaprogramming
- assembly, calling conventions, low level

## What it will conver

- arithmetic operations
- conditionals
- local variables
- function calls
- etc.

## Week 1: Integers

- will use our compiler to produce x86 assembly
- then use gcc to convert it to executable (the assembled and the linker do that)

```s
	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 13
	.globl	_main                   	## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
## BB#0:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	$2, %eax
	popq	%rbp
	retq
                                        ## -- End function

.subsections_via_symbols
```

- `globl _main` means main should be visible to the linker (otherwise can't find entry point)

```s
_main:                  ; label for start of "main" function
    movl    $2, %eax    ; move constant "2" into the EAX register
    ret                 ; return from function
```

- when a function returns, the EAX register will contain its return value
- the `main` function's return value will be the program's exit code

### Strategy

- split the compiler into three stages:
    - lexing
	- parsing
	- code generation
	- this is pretty standard architecture, except you'd normally want a bunch of optimization passes between parsing and code generation

#### Lexing

- Breaks up a string (the source code) into a list of tokens
- Tokens are grouped in categories
- Examples: 
	- `int` keyword
	- Identifier `main`
	- Open paren, Close paren
	- Open brace, Close brace
	- `return` keyword
	- Semicolon
	- Constant `2`

#### Task

Write a `lex` function that accepts a file and returns a list of tokens. It should work for all stage 1 examples in the test suite. The invalid examples should raise errors in the parser, not the lexer. To keep things simple we only lex decimal integers.

#### Parsing

Write a parse function that accepts a list of tokens and returns an AST, rooted at a Program node. 

#### Code generation



### To further search:
- linters, static analyzers, and metaprogramming
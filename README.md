# MyCode

A Python tokenizer library for lexical analysis. This library provides classes for tokenizing source code into lexical tokens, which is useful for building compilers, interpreters, parsers, and text processors.

## Features

- **Token Class**: Represents individual lexical tokens with type, value, and position information
- **Tokenizer Class**: Converts text into a stream of tokens
- Support for multiple token types:
  - Literals (integers, floats, strings)
  - Identifiers and keywords
  - Operators (arithmetic, comparison, assignment)
  - Delimiters (parentheses, brackets, braces, punctuation)
  - Special tokens (newlines, EOF, whitespace)
- Position tracking (line and column numbers)
- Comprehensive test suite

## Installation

Simply copy the `tokenizer.py` file to your project directory.

## Usage

### Basic Example

```python
from tokenizer import Tokenizer

# Create a tokenizer with your input text
code = "x = 42 + 3.14"
tokenizer = Tokenizer(code)

# Get all tokens at once
tokens = tokenizer.tokenize()

for token in tokens:
    print(token)
```

Output:
```
IDENTIFIER('x')
ASSIGN('=')
INTEGER(42)
PLUS('+')
FLOAT(3.14)
```

### Getting Tokens One at a Time

```python
from tokenizer import Tokenizer

tokenizer = Tokenizer("x + y")

token1 = tokenizer.get_next_token()  # IDENTIFIER('x')
token2 = tokenizer.get_next_token()  # PLUS('+')
token3 = tokenizer.get_next_token()  # IDENTIFIER('y')
token4 = tokenizer.get_next_token()  # EOF
```

### Working with Token Objects

```python
from tokenizer import Token, TokenType

token = Token(TokenType.INTEGER, 42, line=0, column=5)

print(token.type)    # TokenType.INTEGER
print(token.value)   # 42
print(token.line)    # 0
print(token.column)  # 5
```

### More Examples

See the `example.py` file for more comprehensive examples, including:
- Function definitions
- Conditional statements
- String literals
- Array/list access
- Token type analysis

Run the examples with:
```bash
python example.py
```

## Supported Token Types

The tokenizer recognizes the following token types:

### Literals
- `INTEGER`: Integer numbers (e.g., `42`, `123`)
- `FLOAT`: Floating-point numbers (e.g., `3.14`, `0.5`)
- `STRING`: String literals (e.g., `"hello"`, `'world'`)
- `IDENTIFIER`: Variable and function names (e.g., `x`, `my_var`)

### Keywords
- `KEYWORD`: Reserved words (e.g., `if`, `else`, `while`, `for`, `return`, `def`, `class`)

### Operators
- Arithmetic: `PLUS` (+), `MINUS` (-), `MULTIPLY` (*), `DIVIDE` (/)
- Assignment: `ASSIGN` (=)
- Comparison: `EQUALS` (==), `NOT_EQUALS` (!=), `LESS_THAN` (<), `GREATER_THAN` (>), `LESS_EQUAL` (<=), `GREATER_EQUAL` (>=)

### Delimiters
- Parentheses: `LPAREN` ((), `RPAREN` ())
- Braces: `LBRACE` ({), `RBRACE` (})
- Brackets: `LBRACKET` ([), `RBRACKET` (])
- Punctuation: `COMMA` (,), `SEMICOLON` (;), `COLON` (:), `DOT` (.)

### Special
- `NEWLINE`: Line breaks
- `EOF`: End of file
- `UNKNOWN`: Unrecognized characters

## Running Tests

The library includes a comprehensive test suite:

```bash
python -m unittest test_tokenizer.py -v
```

## API Reference

### Token Class

```python
Token(token_type: TokenType, value: Any, line: int = 0, column: int = 0)
```

Represents a single lexical token.

**Attributes:**
- `type`: The type of the token (TokenType enum)
- `value`: The value/lexeme of the token
- `line`: Line number where the token appears (0-indexed)
- `column`: Column number where the token starts (0-indexed)

### Tokenizer Class

```python
Tokenizer(text: str)
```

A tokenizer for converting text into tokens.

**Methods:**
- `get_next_token() -> Token`: Get the next token from the input
- `tokenize() -> list[Token]`: Tokenize the entire input text
- `advance() -> None`: Move to the next character
- `peek(offset: int = 1) -> Optional[str]`: Look ahead at the next character

## License

This project is open source and available for use in your projects.
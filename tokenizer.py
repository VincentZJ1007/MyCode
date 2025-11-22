"""
Token module for lexical analysis.

This module provides classes for representing and working with tokens,
which are the basic building blocks of lexical analysis in compilers,
interpreters, and text processors.
"""

from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    """Enumeration of token types."""
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    KEYWORD = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()
    
    # Special
    WHITESPACE = auto()
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()
    UNKNOWN = auto()


class Token:
    """
    Represents a single lexical token.
    
    A token consists of a type, value, and position information.
    """
    
    def __init__(
        self,
        token_type: TokenType,
        value: Any,
        line: int = 0,
        column: int = 0
    ):
        """
        Initialize a Token.
        
        Args:
            token_type: The type of the token
            value: The value/lexeme of the token
            line: Line number where the token appears (0-indexed)
            column: Column number where the token starts (0-indexed)
        """
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        """Return a string representation of the token."""
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"{self.type.name}({self.value!r})"
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another token."""
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.type == other.type and
            self.value == other.value and
            self.line == other.line and
            self.column == other.column
        )
    
    def __hash__(self) -> int:
        """Return hash of the token."""
        return hash((self.type, self.value, self.line, self.column))


class Tokenizer:
    """
    A simple tokenizer for converting text into tokens.
    
    This tokenizer can identify numbers, identifiers, operators,
    and common delimiters.
    """
    
    # Common keywords in many programming languages
    KEYWORDS = {
        'if', 'else', 'while', 'for', 'return', 'function',
        'class', 'def', 'import', 'from', 'as', 'in',
        'true', 'false', 'null', 'none', 'and', 'or', 'not'
    }
    
    def __init__(self, text: str):
        """
        Initialize the tokenizer with input text.
        
        Args:
            text: The input text to tokenize
        """
        self.text = text
        self.pos = 0
        self.line = 0
        self.column = 0
        self.current_char: Optional[str] = self.text[0] if text else None
    
    def advance(self) -> None:
        """Move to the next character in the input."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """
        Look ahead at the next character without advancing.
        
        Args:
            offset: How many characters ahead to look (default: 1)
            
        Returns:
            The character at the offset position, or None if past end
        """
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters (except newlines)."""
        while self.current_char and self.current_char in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        """Read a numeric token (integer or float)."""
        start_line = self.line
        start_column = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    break  # Second dot, stop here
                has_dot = True
            num_str += self.current_char
            self.advance()
        
        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_column)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword token."""
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = TokenType.KEYWORD if identifier.lower() in self.KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, identifier, start_line, start_column)
    
    def read_string(self, quote: str) -> Token:
        """Read a string token."""
        start_line = self.line
        start_column = self.column
        self.advance()  # Skip opening quote
        string_value = ''
        
        while self.current_char and self.current_char != quote:
            if self.current_char == '\\' and self.peek() == quote:
                self.advance()  # Skip backslash
                string_value += self.current_char
                self.advance()
            else:
                string_value += self.current_char
                self.advance()
        
        if self.current_char == quote:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def get_next_token(self) -> Token:
        """
        Get the next token from the input.
        
        Returns:
            The next token, or EOF token if at end of input
        """
        while self.current_char:
            # Skip whitespace
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newline
            if self.current_char == '\n':
                token = Token(TokenType.NEWLINE, '\n', self.line, self.column)
                self.advance()
                return token
            
            # Numbers
            if self.current_char.isdigit():
                return self.read_number()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Strings
            if self.current_char in '"\'':
                return self.read_string(self.current_char)
            
            # Operators and delimiters
            start_line = self.line
            start_column = self.column
            char = self.current_char
            
            # Two-character operators
            if char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQUALS, '==', start_line, start_column)
            
            if char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NOT_EQUALS, '!=', start_line, start_column)
            
            if char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LESS_EQUAL, '<=', start_line, start_column)
            
            if char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GREATER_EQUAL, '>=', start_line, start_column)
            
            # Single-character operators and delimiters
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }
            
            if char in single_char_tokens:
                token_type = single_char_tokens[char]
                self.advance()
                return Token(token_type, char, start_line, start_column)
            
            # Unknown character
            self.advance()
            return Token(TokenType.UNKNOWN, char, start_line, start_column)
        
        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self) -> list[Token]:
        """
        Tokenize the entire input text.
        
        Returns:
            A list of all tokens (excluding EOF)
        """
        tokens = []
        while True:
            token = self.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        return tokens

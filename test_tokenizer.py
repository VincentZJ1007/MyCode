"""
Unit tests for the tokenizer module.
"""

import unittest
from tokenizer import Token, TokenType, Tokenizer


class TestToken(unittest.TestCase):
    """Tests for the Token class."""
    
    def test_token_creation(self):
        """Test creating a token."""
        token = Token(TokenType.INTEGER, 42, 0, 5)
        self.assertEqual(token.type, TokenType.INTEGER)
        self.assertEqual(token.value, 42)
        self.assertEqual(token.line, 0)
        self.assertEqual(token.column, 5)
    
    def test_token_repr(self):
        """Test token string representation."""
        token = Token(TokenType.IDENTIFIER, "x", 1, 2)
        self.assertEqual(repr(token), "Token(IDENTIFIER, 'x', 1:2)")
    
    def test_token_str(self):
        """Test token human-readable string."""
        token = Token(TokenType.PLUS, "+", 0, 0)
        self.assertEqual(str(token), "PLUS('+')")
    
    def test_token_equality(self):
        """Test token equality comparison."""
        token1 = Token(TokenType.INTEGER, 42, 0, 0)
        token2 = Token(TokenType.INTEGER, 42, 0, 0)
        token3 = Token(TokenType.INTEGER, 43, 0, 0)
        
        self.assertEqual(token1, token2)
        self.assertNotEqual(token1, token3)
    
    def test_token_hash(self):
        """Test token hashing."""
        token1 = Token(TokenType.STRING, "hello", 0, 0)
        token2 = Token(TokenType.STRING, "hello", 0, 0)
        
        # Same tokens should have same hash
        self.assertEqual(hash(token1), hash(token2))
        
        # Should be able to use in sets
        token_set = {token1, token2}
        self.assertEqual(len(token_set), 1)


class TestTokenizer(unittest.TestCase):
    """Tests for the Tokenizer class."""
    
    def test_tokenize_empty_string(self):
        """Test tokenizing an empty string."""
        tokenizer = Tokenizer("")
        tokens = tokenizer.tokenize()
        self.assertEqual(tokens, [])
    
    def test_tokenize_integers(self):
        """Test tokenizing integer numbers."""
        tokenizer = Tokenizer("42 123 0")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.INTEGER)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].value, 123)
        self.assertEqual(tokens[2].value, 0)
    
    def test_tokenize_floats(self):
        """Test tokenizing floating-point numbers."""
        tokenizer = Tokenizer("3.14 0.5 123.456")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.FLOAT)
        self.assertEqual(tokens[0].value, 3.14)
        self.assertEqual(tokens[1].value, 0.5)
        self.assertEqual(tokens[2].value, 123.456)
    
    def test_tokenize_dot_not_part_of_number(self):
        """Test that standalone dots are tokenized as DOT, not part of numbers."""
        tokenizer = Tokenizer("x.y")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].type, TokenType.DOT)
        self.assertEqual(tokens[1].value, ".")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].value, "y")
    
    def test_tokenize_identifiers(self):
        """Test tokenizing identifiers."""
        tokenizer = Tokenizer("x variable_name _private count123")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 4)
        for token in tokens:
            self.assertEqual(token.type, TokenType.IDENTIFIER)
        
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].value, "variable_name")
        self.assertEqual(tokens[2].value, "_private")
        self.assertEqual(tokens[3].value, "count123")
    
    def test_tokenize_keywords(self):
        """Test tokenizing keywords."""
        tokenizer = Tokenizer("if else while for return")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 5)
        for token in tokens:
            self.assertEqual(token.type, TokenType.KEYWORD)
        
        self.assertEqual(tokens[0].value, "if")
        self.assertEqual(tokens[1].value, "else")
        self.assertEqual(tokens[2].value, "while")
    
    def test_tokenize_strings(self):
        """Test tokenizing string literals."""
        tokenizer = Tokenizer('"hello" "world" \'single\'')
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")
        self.assertEqual(tokens[1].value, "world")
        self.assertEqual(tokens[2].value, "single")
    
    def test_tokenize_escaped_strings(self):
        """Test tokenizing strings with escaped quotes."""
        tokenizer = Tokenizer('"hello \\"world\\""')
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, 'hello "world"')
    
    def test_tokenize_operators(self):
        """Test tokenizing operators."""
        tokenizer = Tokenizer("+ - * / = == != < > <= >=")
        tokens = tokenizer.tokenize()
        
        expected_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.ASSIGN,
            TokenType.EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_tokenize_delimiters(self):
        """Test tokenizing delimiters."""
        tokenizer = Tokenizer("( ) { } [ ] , ; : .")
        tokens = tokenizer.tokenize()
        
        expected_types = [
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.RBRACE,
            TokenType.LBRACKET,
            TokenType.RBRACKET,
            TokenType.COMMA,
            TokenType.SEMICOLON,
            TokenType.COLON,
            TokenType.DOT,
        ]
        
        self.assertEqual(len(tokens), len(expected_types))
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(tokens[i].type, expected_type)
    
    def test_tokenize_newlines(self):
        """Test tokenizing newlines."""
        tokenizer = Tokenizer("x\ny\nz")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.NEWLINE)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.NEWLINE)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)
    
    def test_tokenize_complex_expression(self):
        """Test tokenizing a complex expression."""
        tokenizer = Tokenizer("x = 42 + 3.14")
        tokens = tokenizer.tokenize()
        
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)
        self.assertEqual(tokens[2].type, TokenType.INTEGER)
        self.assertEqual(tokens[2].value, 42)
        self.assertEqual(tokens[3].type, TokenType.PLUS)
        self.assertEqual(tokens[4].type, TokenType.FLOAT)
        self.assertEqual(tokens[4].value, 3.14)
    
    def test_tokenize_function_definition(self):
        """Test tokenizing a function definition."""
        code = "def add(x, y):"
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.KEYWORD)
        self.assertEqual(tokens[0].value, "def")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "add")
        self.assertEqual(tokens[2].type, TokenType.LPAREN)
        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].value, "x")
        self.assertEqual(tokens[4].type, TokenType.COMMA)
        self.assertEqual(tokens[5].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[5].value, "y")
        self.assertEqual(tokens[6].type, TokenType.RPAREN)
        self.assertEqual(tokens[7].type, TokenType.COLON)
    
    def test_position_tracking(self):
        """Test that position tracking works correctly."""
        code = "x = 42\ny = 10"
        tokenizer = Tokenizer(code)
        tokens = tokenizer.tokenize()
        
        # First line
        self.assertEqual(tokens[0].line, 0)  # x
        self.assertEqual(tokens[0].column, 0)
        self.assertEqual(tokens[1].line, 0)  # =
        self.assertEqual(tokens[2].line, 0)  # 42
        self.assertEqual(tokens[3].line, 0)  # \n
        
        # Second line
        self.assertEqual(tokens[4].line, 1)  # y
        self.assertEqual(tokens[4].column, 0)
        self.assertEqual(tokens[5].line, 1)  # =
        self.assertEqual(tokens[6].line, 1)  # 10
    
    def test_get_next_token(self):
        """Test getting tokens one at a time."""
        tokenizer = Tokenizer("x + y")
        
        token1 = tokenizer.get_next_token()
        self.assertEqual(token1.type, TokenType.IDENTIFIER)
        self.assertEqual(token1.value, "x")
        
        token2 = tokenizer.get_next_token()
        self.assertEqual(token2.type, TokenType.PLUS)
        
        token3 = tokenizer.get_next_token()
        self.assertEqual(token3.type, TokenType.IDENTIFIER)
        self.assertEqual(token3.value, "y")
        
        token4 = tokenizer.get_next_token()
        self.assertEqual(token4.type, TokenType.EOF)
    
    def test_peek(self):
        """Test peeking ahead in the input."""
        tokenizer = Tokenizer("abc")
        self.assertEqual(tokenizer.current_char, 'a')
        self.assertEqual(tokenizer.peek(), 'b')
        self.assertEqual(tokenizer.peek(2), 'c')
        self.assertIsNone(tokenizer.peek(3))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Example usage of the tokenizer module.

This script demonstrates how to use the Token and Tokenizer classes
to perform lexical analysis on source code.
"""

from tokenizer import Tokenizer, TokenType


def main():
    """Run examples of the tokenizer."""
    
    print("=" * 60)
    print("Token Example: Simple Expression")
    print("=" * 60)
    
    # Example 1: Simple mathematical expression
    code1 = "x = 42 + 3.14"
    print(f"\nInput: {code1}")
    print("Tokens:")
    
    tokenizer1 = Tokenizer(code1)
    tokens1 = tokenizer1.tokenize()
    
    for token in tokens1:
        print(f"  {token}")
    
    print("\n" + "=" * 60)
    print("Token Example: Function Definition")
    print("=" * 60)
    
    # Example 2: Function definition
    code2 = """def add(x, y):
    return x + y"""
    
    print(f"\nInput:\n{code2}")
    print("\nTokens:")
    
    tokenizer2 = Tokenizer(code2)
    tokens2 = tokenizer2.tokenize()
    
    for token in tokens2:
        print(f"  {token} at line {token.line}, column {token.column}")
    
    print("\n" + "=" * 60)
    print("Token Example: Conditional Statement")
    print("=" * 60)
    
    # Example 3: Conditional statement
    code3 = "if x >= 10 and y != 0:"
    print(f"\nInput: {code3}")
    print("Tokens:")
    
    tokenizer3 = Tokenizer(code3)
    tokens3 = tokenizer3.tokenize()
    
    for token in tokens3:
        print(f"  {token}")
    
    print("\n" + "=" * 60)
    print("Token Example: String Literals")
    print("=" * 60)
    
    # Example 4: String literals
    code4 = '"hello" + "world"'
    print(f"\nInput: {code4}")
    print("Tokens:")
    
    tokenizer4 = Tokenizer(code4)
    tokens4 = tokenizer4.tokenize()
    
    for token in tokens4:
        print(f"  {token}")
    
    print("\n" + "=" * 60)
    print("Token Example: Array/List Access")
    print("=" * 60)
    
    # Example 5: Array access
    code5 = "array[0] = values[i + 1]"
    print(f"\nInput: {code5}")
    print("Tokens:")
    
    tokenizer5 = Tokenizer(code5)
    tokens5 = tokenizer5.tokenize()
    
    for token in tokens5:
        print(f"  {token}")
    
    print("\n" + "=" * 60)
    print("Analyzing Token Types")
    print("=" * 60)
    
    # Count token types in a complex expression
    code6 = "result = (a + b) * (c - d) / 2.5"
    print(f"\nInput: {code6}")
    
    tokenizer6 = Tokenizer(code6)
    tokens6 = tokenizer6.tokenize()
    
    # Count tokens by type
    type_counts = {}
    for token in tokens6:
        type_name = token.type.name
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    
    print("\nToken type distribution:")
    for token_type, count in sorted(type_counts.items()):
        print(f"  {token_type}: {count}")


if __name__ == "__main__":
    main()

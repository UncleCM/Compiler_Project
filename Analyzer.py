import re
import sys

TOKEN_PATTERNS = [
    ('REAL', r'\d+\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+'),  # Real numbers (decimal or scientific)
    ('INT', r'\d+'),                                        # Integers
    ('LIST', r'list'),                                      # List keyword
    ('GTE', r'>='),                                         # Greater than or equal
    ('LTE', r'<='),                                         # Less than or equal
    ('EQ', r'=='),                                          # Equal to
    ('NEQ', r'!='),                                         # Not equal to
    ('INTDIV', r'//'),                                      # Integer division
    ('GT', r'>'),                                           # Greater than
    ('LT', r'<'),                                           # Less than
    ('PLUS', r'\+'),                                        # Addition
    ('MINUS', r'-'),                                        # Subtraction
    ('MUL', r'\*'),                                         # Multiplication
    ('DIV', r'/'),                                          # Division
    ('POW', r'\^'),                                         # Exponent
    ('ASSIGN', r'='),                                       # Assignment
    ('LPAREN', r'\('),                                      # Left parenthesis
    ('RPAREN', r'\)'),                                      # Right parenthesis
    ('LBRACKET', r'\['),                                    # Left bracket
    ('RBRACKET', r'\]'),                                    # Right bracket
    ('VAR', r'[a-zA-Z][a-zA-Z0-9_]*'),                     # Variables
    ('WHITESPACE', r'[ \t]+'),                              # Whitespace (to skip)
    ('ERR', r'[^\s]'),                                      # Error token (any other character)
]

master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)
token_regex = re.compile(master_pattern)

def tokenize_line(line):
    tokens = []
    pos = 0
    while pos < len(line):
        match = token_regex.match(line, pos)
        if match:
            token_type = match.lastgroup
            token_value = match.group()
            
            if token_type != 'WHITESPACE':
                match token_type:
                    case 'PLUS':
                        tokens.append((token_value, '+'))
                    case 'MINUS':
                        tokens.append((token_value, '-'))
                    case 'MUL':
                        tokens.append((token_value, '*'))
                    case 'DIV':
                        tokens.append((token_value, '/'))
                    case 'INTDIV':
                        tokens.append((token_value, '//'))
                    case 'POW':
                        tokens.append((token_value, 'POW'))
                    case 'GT':
                        tokens.append((token_value, '>'))
                    case 'GTE':
                        tokens.append((token_value, '>='))
                    case 'LT':
                        tokens.append((token_value, '<'))
                    case 'LTE':
                        tokens.append((token_value, '<='))
                    case 'EQ':
                        tokens.append((token_value, '=='))
                    case 'NEQ':
                        tokens.append((token_value, '!='))
                    case 'ASSIGN':
                        tokens.append((token_value, '='))
                    case 'LPAREN':
                        tokens.append((token_value, 'LPAREN'))
                    case 'RPAREN':
                        tokens.append((token_value, 'RPAREN'))
                    case 'LBRACKET':
                        tokens.append((token_value, 'LBRACKET'))
                    case 'RBRACKET':
                        tokens.append((token_value, 'RBRACKET'))
                    case 'LIST':
                        tokens.append((token_value, 'list'))
                    case 'ERR':
                        tokens.append((token_value, 'ERR'))
                    case _:  # default case
                        tokens.append((token_value, token_type))
            
            pos = match.end()
        else:
            pos += 1
    
    return tokens

def format_tokens(tokens):
    """Format tokens for output"""
    return ' '.join(f'{token}/{token_type}' for token, token_type in tokens)

def main():
    if len(sys.argv) < 2:
        print("Usage: python lexer.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    else:
        base_name = input_file.rsplit('.', 1)[0]
        output_file = base_name + '.tok'
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.rstrip('\n\r')  
                if line.strip(): 
                    tokens = tokenize_line(line)
                    output = format_tokens(tokens)
                    outfile.write(output + '\n')
                else:
                    outfile.write('\n') 
        
        print(f"Tokenization complete. Output written to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
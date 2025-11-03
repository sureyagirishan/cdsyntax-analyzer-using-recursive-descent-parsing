# backend/parser.py
# A basic recursive descent parser for simple arithmetic expressions
# Grammar:
#   expr   -> term (("+" | "-") term)*
#   term   -> factor (("*" | "/") factor)*
#   factor -> NUMBER | "(" expr ")"

import re
from dataclasses import dataclass
from typing import List, Optional

TOKEN_REGEX = re.compile(r"\s*(?:(?P<NUMBER>\d+(?:\.\d+)?)|(?P<PLUS>\+)|(?P<MINUS>\-)|(?P<MUL>\*)|(?P<DIV>/)|(?P<LPAREN>\()|(?P<RPAREN>\)))")

@dataclass
class Token:
    type: str
    value: str

@dataclass
class ASTNode:
    type: str
    value: Optional[str] = None
    children: Optional[List['ASTNode']] = None

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < len(self.text):
            m = TOKEN_REGEX.match(self.text, self.pos)
            if not m:
                raise SyntaxError(f"Unexpected character at position {self.pos}: '{self.text[self.pos]}'")
            self.pos = m.end()
            kind = m.lastgroup
            if kind is None:
                continue
            value = m.group(kind)
            mapping = {
                'NUMBER': ('NUMBER', value),
                'PLUS': ('PLUS', '+'),
                'MINUS': ('MINUS', '-'),
                'MUL': ('MUL', '*'),
                'DIV': ('DIV', '/'),
                'LPAREN': ('LPAREN', '('),
                'RPAREN': ('RPAREN', ')'),
            }
            ttype, tval = mapping[kind]
            tokens.append(Token(ttype, tval))
        tokens.append(Token('EOF', ''))
        return tokens

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def advance(self) -> Token:
        tok = self.tokens[self.current]
        self.current += 1
        return tok

    def match(self, *types: str) -> bool:
        if self.peek().type in types:
            self.advance()
            return True
        return False

    def parse_expr(self) -> ASTNode:
        node = self.parse_term()
        while self.peek().type in ('PLUS', 'MINUS'):
            op = self.advance()
            right = self.parse_term()
            node = ASTNode('BINOP', op.value, [node, right])
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.peek().type in ('MUL', 'DIV'):
            op = self.advance()
            right = self.parse_factor()
            node = ASTNode('BINOP', op.value, [node, right])
        return node

    def parse_factor(self) -> ASTNode:
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.advance()
            return ASTNode('NUMBER', tok.value)
        if tok.type == 'LPAREN':
            self.advance()
            expr = self.parse_expr()
            if not self.match('RPAREN'):
                raise SyntaxError("Expected ')'")
            return expr
        raise SyntaxError(f"Unexpected token: {tok.type}")

    def parse(self) -> ASTNode:
        ast = self.parse_expr()
        if self.peek().type != 'EOF':
            raise SyntaxError(f"Unexpected token after expression: {self.peek().type}")
        return ast


def parse_expression(text: str) -> ASTNode:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def ast_to_dict(node: ASTNode) -> dict:
    return {
        'type': node.type,
        'value': node.value,
        'children': [ast_to_dict(c) for c in (node.children or [])]
    }

if __name__ == '__main__':
    import json
    import sys
    expr = sys.argv[1] if len(sys.argv) > 1 else "1 + 2*(3-4/2)"
    try:
        ast = parse_expression(expr)
        print(json.dumps(ast_to_dict(ast), indent=2))
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)

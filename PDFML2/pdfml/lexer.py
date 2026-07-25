import re

class TokenType:
    TEXT = "TEXT"
    LBRACE = "LBRACE"      # {
    RBRACE = "RBRACE"      # }
    SLASH = "SLASH"        # /
    EQUALS = "EQUALS"      # =
    IDENT = "IDENT"        # nama tag / atribut
    STRING = "STRING"      # "teks"
    NUMBER = "NUMBER"      # 123 atau 12.5
    EOF = "EOF"

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.col = 1
        self.in_tag = False

    def advance(self, steps=1):
        for _ in range(steps):
            if self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1

    def peek(self):
        if self.pos < len(self.source):
            return self.source[self.pos]
        return None

    def get_tokens(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.peek()
            
            # MODE 1: Di luar kurung kurawal (TEXT)
            if not self.in_tag:
                start_pos = self.pos
                text_val = ""
                while self.pos < len(self.source) and self.peek() != '{':
                    text_val += self.peek()
                    self.advance()
                
                if text_val:
                    # Hanya simpan teks jika bukan sekadar whitespace kosong
                    if text_val.strip():
                        tokens.append(Token(TokenType.TEXT, text_val, self.line, self.col))
                
                if self.pos < len(self.source) and self.peek() == '{':
                    tokens.append(Token(TokenType.LBRACE, "{", self.line, self.col))
                    self.advance()
                    self.in_tag = True
                continue

            # MODE 2: Di dalam kurung kurawal (TAG)
            if char.isspace():
                self.advance()
                continue
                
            if char == '}':
                tokens.append(Token(TokenType.RBRACE, "}", self.line, self.col))
                self.advance()
                self.in_tag = False
            elif char == '/':
                tokens.append(Token(TokenType.SLASH, "/", self.line, self.col))
                self.advance()
            elif char == '=':
                tokens.append(Token(TokenType.EQUALS, "=", self.line, self.col))
                self.advance()
            elif char == '"':
                self.advance() # skip petik awal
                string_val = ""
                while self.peek() is not None and self.peek() != '"':
                    string_val += self.peek()
                    self.advance()
                if self.peek() is None:
                    raise LexerError(f"String tidak ditutup pada baris {self.line}")
                self.advance() # skip petik akhir
                tokens.append(Token(TokenType.STRING, string_val, self.line, self.col))
            elif char.isalpha() or char == '_':
                ident_val = ""
                while self.peek() is not None and (self.peek().isalnum() or self.peek() == '_'):
                    ident_val += self.peek()
                    self.advance()
                tokens.append(Token(TokenType.IDENT, ident_val.lower(), self.line, self.col))
            elif char.isdigit():
                num_val = ""
                while self.peek() is not None and (self.peek().isdigit() or self.peek() == '.'):
                    num_val += self.peek()
                    self.advance()
                tokens.append(Token(TokenType.NUMBER, float(num_val) if '.' in num_val else int(num_val), self.line, self.col))
            else:
                raise LexerError(f"Karakter ilegal '{char}' di dalam tag pada baris {self.line}, kolom {self.col}")
                
        tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return tokens

from .lexer import TokenType, Lexer, Token

class ASTNode: pass

class ElementNode(ASTNode):
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children
    
    def __repr__(self):
        return f"<{self.tag} {self.attrs}>" + "".join(repr(c) for c in self.children) + f"</{self.tag}>"

class TextNode(ASTNode):
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return f"TEXT({self.text.strip()!r})"

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current().type == token_type:
            token = self.current()
            self.pos += 1
            return token
        raise ParserError(f"Syntax Error: Diharapkan {token_type} tapi mendapat {self.current().type} di baris {self.current().line}")

    def parse(self):
        nodes = []
        while self.current().type != TokenType.EOF:
            nodes.append(self.parse_node())
        return nodes

    def parse_node(self):
        if self.current().type == TokenType.TEXT:
            val = self.current().value
            self.eat(TokenType.TEXT)
            return TextNode(val)
        elif self.current().type == TokenType.LBRACE:
            return self.parse_element()
        else:
            raise ParserError(f"Token tak terduga {self.current().value} di baris {self.current().line}")

    def parse_element(self):
        self.eat(TokenType.LBRACE)
        
        # Mengecek apakah ini tag penutup yang salah letak (contoh: {/body})
        if self.current().type == TokenType.SLASH:
            raise ParserError(f"Tag penutup tanpa tag pembuka di baris {self.current().line}")
            
        tag_name = self.eat(TokenType.IDENT).value
        attrs = {}

        # Parse Atribut
        while self.current().type in (TokenType.IDENT, TokenType.STRING):
            attr_name = self.eat(TokenType.IDENT).value
            self.eat(TokenType.EQUALS)
            
            if self.current().type == TokenType.STRING:
                attr_val = self.eat(TokenType.STRING).value
            elif self.current().type == TokenType.NUMBER:
                attr_val = self.eat(TokenType.NUMBER).value
            else:
                raise ParserError(f"Nilai atribut invalid pada baris {self.current().line}")
                
            attrs[attr_name] = attr_val

        # Cek Self Closing tag (contoh: {image src="logo.png" /})
        if self.current().type == TokenType.SLASH:
            self.eat(TokenType.SLASH)
            self.eat(TokenType.RBRACE)
            return ElementNode(tag_name, attrs, [])

        self.eat(TokenType.RBRACE)
        
        # Parse Children (Isi dalam tag)
        children = []
        while self.current().type != TokenType.EOF:
            if self.current().type == TokenType.LBRACE and self.tokens[self.pos + 1].type == TokenType.SLASH:
                break # Ketemu closing tag
            children.append(self.parse_node())
            
        # Parse Closing tag
        self.eat(TokenType.LBRACE)
        self.eat(TokenType.SLASH)
        close_tag = self.eat(TokenType.IDENT).value
        self.eat(TokenType.RBRACE)
        
        if close_tag != tag_name:
            raise ParserError(f"Mismatched tag! Diharapkan {{/{tag_name}}} tapi mendapat {{/{close_tag}}}")
            
        return ElementNode(tag_name, attrs, children)

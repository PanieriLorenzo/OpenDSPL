import re
from enum import Enum

class Token_Type(Enum):
    ERR = -1
    EOF = 0
    WHITESPACE = 5
    COMMENT = 10
    IDENTIFIER = 20
    DECLARATION = 30
    TYPE_BYTE = 50
    TYPE_I16 = 55
    TYPE_I24 = 60
    TYPE_I32 = 70
    TYPE_I64 = 75
    TYPE_U16 = 77
    TYPE_U24 = 80
    TYPE_U32 = 90
    TYPE_U64 = 95
    TYPE_F32 = 100
    TYPE_F64 = 110
    TYPE_BOOL = 120
    TYPE_NUMBER = 130
    TYPE_RECORD = 131
    TYPE_PROCESS = 132
    TYPE_MODULE = 133
    COMMA = 135
    OPEN_PAREN = 140
    CLOSE_PAREN = 150
    OPEN_BRACKET = 155
    CLOSE_BRACKET = 160
    OPEN_BRACE = 170
    CLOSE_BRACE = 180
    SEMICOLON = 185
    LITER_INT = 190
    LITER_FLOAT = 195
    LITER_BOOL = 200
    LITER_CHAR = 210
    LITER_STR = 215
    OP_ASSIGN = 220
    OP_ADD = 230
    OP_SUB = 240
    OP_MUL = 250
    OP_POW = 255
    OP_DIV = 260
    OP_MOD = 270
    OP_DELAY = 280
    OP_BIT_AND = 290
    OP_BIT_OR = 300
    OP_BIT_NOT = 310
    OP_BIT_XOR = 320
    OP_BIT_LSH = 330
    OP_BIT_RSH = 340
    OP_BOOL_AND = 350
    OP_BOOL_OR = 360
    OP_BOOL_NOT = 370
    OP_CMP_GREAT = 380
    OP_CMP_GEQ = 390
    OP_CMP_EQ = 400
    OP_CMP_LESS = 410
    OP_CMP_LEQ = 420
    OP_CMP_NEQ = 430
    ARROW = 440
    DOT = 450
    IMPORT = 460
    ATTACH = 470
    RETURN = 480

class Token:
    def __init__(self, value, t_type):

        # type of token
        self.type = t_type

        # value of the token, numbers for literals, strings for identifiers
        # unused for tokens without value
        self.value = value

class Tokenizer:
    def __init__(self, string):
        self.string = string

    def nextToken(self) -> Token:
        # check if empty
        if len(self.string) <= 0:
            return Token(None, Token_Type.EOF)

        # match COMMENT
        #   skip
        if match := re.match(r"#.*", self.string):
            self.string = self.string[len(match.group()):]
            return self.nextToken()
        
        # match WHITESPACE
        #   skip
        if match := re.match(r"\s+", self.string):
            self.string = self.string[len(match.group()):]
            return self.nextToken()
        
        # match IMPORT
        #   valueless token
        if match := re.match(r"(?<!\w)import(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.IMPORT)
        
        # match ATTACH
        #   valueless token
        if match := re.match(r"(?<!\w)attach(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.ATTACH)

        # match RETURN
        #   valueless token
        if match := re.match(r"(?<!\w)return(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.RETURN)
        
        # match DOT
        #   valueless token
        if match := re.match(r"\.", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.DOT)
        
        # match DECLARATION
        #   valueless token
        if match := re.match(r":", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.DECLARATION)
        
        # match COMMA
        #   valueless token
        if match := re.match(r",", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.COMMA)
        
        # match SEMICOLON
        #   valueless token
        if match := re.match(r";", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.SEMICOLON)

        # match TYPE_BYTE
        #   valueless token
        if match := re.match(r"(?<!\w)byte(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_BYTE)
        
        # match TYPE_I16
        #   valueless token
        if match := re.match(r"(?<!\w)i16(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_I16)
        
        # match TYPE_I24
        #   valueless token
        if match := re.match(r"(?<!\w)i24(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_I24)
        
        # match TYPE_I32
        #   valueless token
        if match := re.match(r"(?<!\w)i32(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_I32)
        
        # match TYPE_I64
        #   valueless token
        if match := re.match(r"(?<!\w)i64(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_I64)
        
        # match TYPE_U16
        #   valueless token
        if match := re.match(r"(?<!\w)u16(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_U16)
        
        # match TYPE_U24
        #   valueless token
        if match := re.match(r"(?<!\w)u24(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_U24)
        
        # match TYPE_U32
        #   valueless token
        if match := re.match(r"(?<!\w)u32(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_U32)
        
        # match TYPE_U64
        #   valueless token
        if match := re.match(r"(?<!\w)u64(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_U64)
        
        # match TYPE_F32
        #   valueless token
        if match := re.match(r"(?<!\w)f32(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_F32)
        
        # match TYPE_F64
        #   valueless token
        if match := re.match(r"(?<!\w)f64(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_F64)
        
        # match TYPE_BOOL
        #   valueless token
        if match := re.match(r"(?<!\w)bool(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_BOOL)
        
        # match TYPE_NUMBER
        #   valueless token
        if match := re.match(r"(?<!\w)number(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_NUMBER)
        
        # match TYPE_RECORD
        #   valueless token
        if match := re.match(r"(?<!\w)record(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_RECORD)
        
        # match TYPE_PROCESS
        #   valueless token
        if match := re.match(r"(?<!\w)process(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_PROCESS)
        
        # match TYPE_MODULE
        #   valueless token
        if match := re.match(r"(?<!\w)module(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.TYPE_MODULE)
        
        # match OPEN_PAREN
        #   valueless token
        if match := re.match(r"\(", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OPEN_PAREN)
        
        # match CLOSE_PAREN
        #   valueless token
        if match := re.match(r"\)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.CLOSE_PAREN)
        
        # match OPEN_BRACKET
        #   valueless token
        if match := re.match(r"\[", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OPEN_BRACKET)
        
        # match CLOSE_BRACKET
        #   valueless token
        if match := re.match(r"\]", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.CLOSE_BRACKET)
        
        # match OPEN_BRACE
        #   valueless token
        if match := re.match(r"\{", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OPEN_BRACE)
        
        # match CLOSE_BRACE
        #   valueless token
        if match := re.match(r"\}", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.CLOSE_BRACE)
        
        # match LITER_INT
        #   parse value
        if match := re.match(r"(?<!\w)-?[0-9]+(?![\w\.])", self.string):
            self.string = self.string[len(match.group()):]
            return Token(int(match.group()), Token_Type.LITER_INT)
        
        # match LITER_FLOAT
        #   parse value
        if match := re.match(r"(?<!\w)-?[0-9]*\.[0-9]+(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(float(match.group()), Token_Type.LITER_FLOAT)
        
        # match LITER_BOOL
        #   value is either true or false
        if match := re.match(r"(?<!\w)true(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(True, Token_Type.LITER_BOOL)
        if match := re.match(r"(?<!\w)false(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(True, Token_Type.LITER_BOOL)
        
        # match LITER_CHAR
        #   return parsed ASCII value
        if match := re.match(r"'([^']|\\')?'", self.string):
            self.string = self.string[len(match.group()):]
            return Token(match.group()[1], Token_Type.LITER_CHAR)
        
        # match LITER_STR
        #   return raw string
        if match := re.match(r'(?<!\\)".*?(?<!\\)"', self.string):
            length = len(match.group())
            self.string = self.string[length:]
            return Token(match.group()[1:length-1], Token_Type.LITER_STR)
        
        # match OP_ASSIGN
        #   valueless token, avoid matching ==
        if match := re.match(r"(?<!=)=(?!=)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_ASSIGN)

        # match OP_ADD
        #   valueless token
        if match := re.match(r"\+", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_ADD)
        
        # match OP_SUB
        #   valueless token, avoid matching ->
        if match := re.match(r"-(?!>)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_SUB)
        
        # match OP_MUL
        #   valueless token, avoid matching **
        if match := re.match(r"(?<!\*)\*(?!\*)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_MUL)
        
        # match OP_POW
        #   valueless token
        if match := re.match(r"\*\*", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_POW)
        
        # match OP_DIV
        #   valueless token
        if match := re.match(r"/", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_DIV)
        
        # match OP_MOD
        #   valueless token
        if match := re.match(r"%", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_MOD)
        
        # match OP_DELAY
        #   valueless token
        if match := re.match(r"@", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_DELAY)
        
        # match OP_BIT_AND
        #   valueless token
        if match := re.match(r"&", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_AND)
        
        # match OP_BIT_OR
        #   valueless token
        if match := re.match(r"\|", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_OR)
        
        # match OP_BIT_NOT
        #   valueless token
        if match := re.match(r"~", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_NOT)
        
        # match OP_BIT_XOR
        #   valueless token
        if match := re.match(r"\^", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_XOR)
        
        # match OP_BIT_LSH
        #   valueless token
        if match := re.match(r"<<", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_LSH)
        
        # match OP_BIT_RSH
        #   valueless token
        if match := re.match(r">>", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BIT_RSH)
        
        # match OP_BOOL_AND
        #   valueless token
        if match := re.match(r"(?<!\w)and(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BOOL_AND)
        
        # match OP_BOOL_OR
        #   valueless token
        if match := re.match(r"(?<!\w)or(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BOOL_AND)
        
        # match OP_BOOL_NOT
        #   valueless token
        if match := re.match(r"(?<!\w)not(?!\w)", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_BOOL_NOT)
        
        # match OP_CMP_GREAT
        #   valueless token, avoid matching >> or >=
        if match := re.match(r"(?<!>)>(?![>=])", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_GREAT)
        
        # match OP_CMP_GEQ
        #   valueless token
        if match := re.match(r">=", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_GEQ)
        
        # match OP_CMP_LESS
        #   valueless token, avoid matching << or <=
        if match := re.match(r"(?<!<)<(?![<=])", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_LESS)
        
        # match OP_CMP_LEQ
        #   valueless token
        if match := re.match(r"<=", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_LEQ)
        
        # match OP_CMP_EQ
        #   valueless token
        if match := re.match(r"==", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_EQ)
        
        # match OP_CMP_NEQ
        #   valueless token
        if match := re.match(r"!=", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.OP_CMP_NEQ)
        
        # match ARROW
        #   valueless token
        if match := re.match(r"->", self.string):
            self.string = self.string[len(match.group()):]
            return Token(None, Token_Type.ARROW)
        
        # match IDENTIFIER
        #   the value is the raw string (name of identifier)
        if match := re.match(r"[a-zA-Z_]+\w*", self.string):
            self.string = self.string[len(match.group()):]
            return Token(match.group(), Token_Type.IDENTIFIER)

        # if nothing matches, return error
        return Token(None, Token_Type.ERR)

    def dbg(self):
        return self.string













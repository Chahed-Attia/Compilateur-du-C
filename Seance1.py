from dataclasses import dataclass
from enum import Enum, auto

class TokType(Enum):
    TOK_IF = auto()
    TOK_ELSE = auto()
    TOK_FOR = auto()
    TOK_WHILE = auto()
    TOK_DO = auto()
    TOK_INT = auto()
    TOK_VOID = auto()
    TOK_CONTINUE = auto()
    TOK_BREAK = auto()
    TOK_RETURN = auto()
    TOK_CONST = auto()
    TOK_IDENT = auto()
    TOK_PLUS = auto()
    TOK_MINUS = auto()
    TOK_MUL = auto()
    TOK_DIV = auto()
    TOK_MOD = auto()
    TOK_AND = auto()
    TOK_LT = auto()
    TOK_GT = auto()
    TOK_LE = auto()
    TOK_GE = auto()
    TOK_EQ = auto()
    TOK_NEQ = auto()
    TOK_ASSIGN = auto()
    TOK_ANDAND = auto()
    TOK_OROR = auto()
    TOK_NOT = auto()
    TOK_LPAREN = auto()
    TOK_RPAREN = auto()
    TOK_LBRACE = auto()
    TOK_RBRACE = auto()
    TOK_LBRACKET = auto()
    TOK_RBRACKET = auto()
    TOK_COMMA = auto()
    TOK_SEMI = auto()
    TOK_EOS = auto()

MOTS_CLES = {
    "if": TokType.TOK_IF, "else": TokType.TOK_ELSE, "for": TokType.TOK_FOR,
    "while": TokType.TOK_WHILE, "do": TokType.TOK_DO, "int": TokType.TOK_INT,
    "void": TokType.TOK_VOID, "continue": TokType.TOK_CONTINUE,
    "break": TokType.TOK_BREAK, "return": TokType.TOK_RETURN,
}

@dataclass
class Token:
    type: TokType
    valeur: int = 0
    ident: str = ""

# --- Variables globales : l'état du lexer traîne partout ---
code = ""
pos = 0
last = None
courant = None


def init(c):
    global code, pos, last, courant
    code = c
    pos = 0
    last = None
    courant = None
    next()


def caractere_courant():
    global pos, code
    if pos < len(code):
        return code[pos]
    return None


def avancer():
    global pos
    c = caractere_courant()
    pos += 1
    return c


def sauter_les_espaces():
    while caractere_courant() is not None and caractere_courant().isspace():
        avancer()


def next():
    global last, courant
    last = courant
    sauter_les_espaces()

    c = caractere_courant()

    if c is None:
        courant = Token(TokType.TOK_EOS)
        return

    if c.isdigit():
        nombre = ""
        while caractere_courant() is not None and caractere_courant().isdigit():
            nombre += avancer()
        courant = Token(TokType.TOK_CONST, valeur=int(nombre))
        return

    if c.isalpha() or c == "_":
        ident = ""
        while caractere_courant() is not None and (caractere_courant().isalnum() or caractere_courant() == "_"):
            ident += avancer()
        if ident in MOTS_CLES:
            courant = Token(MOTS_CLES[ident])
        else:
            courant = Token(TokType.TOK_IDENT, ident=ident)
        return

    deux = code[pos:pos+2]
    deux_car = {
        "<=": TokType.TOK_LE, ">=": TokType.TOK_GE,
        "==": TokType.TOK_EQ, "!=": TokType.TOK_NEQ,
        "&&": TokType.TOK_ANDAND, "||": TokType.TOK_OROR,
    }
    if deux in deux_car:
        avancer(); avancer()
        courant = Token(deux_car[deux])
        return

    un_car = {
        "+": TokType.TOK_PLUS, "-": TokType.TOK_MINUS,
        "*": TokType.TOK_MUL, "/": TokType.TOK_DIV,
        "%": TokType.TOK_MOD, "&": TokType.TOK_AND,
        "<": TokType.TOK_LT, ">": TokType.TOK_GT,
        "=": TokType.TOK_ASSIGN, "!": TokType.TOK_NOT,
        "(": TokType.TOK_LPAREN, ")": TokType.TOK_RPAREN,
        "{": TokType.TOK_LBRACE, "}": TokType.TOK_RBRACE,
        "[": TokType.TOK_LBRACKET, "]": TokType.TOK_RBRACKET,
        ",": TokType.TOK_COMMA, ";": TokType.TOK_SEMI,
    }
    if c in un_car:
        avancer()
        courant = Token(un_car[c])
        return

    raise SyntaxError(f"Caractère inattendu '{c}'")


def check(type_attendu):
    global courant
    if courant.type == type_attendu:
        next()
        return True
    return False


# --- Utilisation ---
init("int x = 5 + 3;")
while courant.type != TokType.TOK_EOS:
    print(courant)
    next()


    
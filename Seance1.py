from dataclasses import dataclass, field
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



# ---------- Arbre ----------
class NodeType(Enum):
    ND_CONST = auto()
    ND_NEG = auto()
    ND_ADD = auto()
    ND_SUB = auto()
    ND_MUL = auto()
    ND_DIV = auto()
    ND_MOD = auto()

@dataclass
class Node:
    type: NodeType
    valeur: int = 0
    ident: str = ""
    ligne: int = 0
    enfants: list = field(default_factory=list)

def node(type):              return Node(type)
def node_v(type, valeur):    return Node(type, valeur=valeur)
def node_i(type, ident):     return Node(type, ident=ident)
def node_1(type, e1):        return Node(type, enfants=[e1])
def node_2(type, e1, e2):    return Node(type, enfants=[e1, e2])
def ajouter_enfant(parent, enfant):
    parent.enfants.append(enfant)

# ---------- Erreurs / accept ----------
def erreur(msg):
    raise SyntaxError(msg)

def accept(type_attendu):
    if not check(type_attendu):
        erreur(f"Attendu {type_attendu}, trouvé {courant.type}")

# ---------- Analyse syntaxique ----------
def A():
    if check(TokType.TOK_CONST):
        return node_v(NodeType.ND_CONST, last.valeur)
    if check(TokType.TOK_LPAREN):
        e = E()
        accept(TokType.TOK_RPAREN)
        return e
    erreur("Atome attendu")

def E():
    return A()          # pour l'instant juste un atome, on étendra après

def I():
    e = E()
    accept(TokType.TOK_SEMI)
    return e

def F():
    return I()

def AnaSynt():
    return F()

def AnaSem():
    return AnaSynt()

# ---------- Génération de code ----------
def gennode(N):
    if N.type == NodeType.ND_CONST:
        print(f"push {N.valeur}")     # à remplacer par l'instruction de ta machine

def gencode():
    A_ = AnaSem()
    print(".start")
    gennode(A_)
    print("dbg")
    print("halt")




    
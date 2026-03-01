from enum import Enum, auto

class TokenType(Enum):
    CONECTIVO = auto()
    PROPOSICAO = auto()

class ConectivoLogico(Enum):
    E = "e"
    OU = "ou"
    CONDICIONAL = "se...entao"
    BICONDICIONAL = "se e somente se"
    NEGACAO = "nao"

class ClassificacaoLogica(Enum):
    TAUTOLOGIA = "Tautologia"
    CONTRADICAO = "Contradição"
    CONTINGENCIA = "Contingência"
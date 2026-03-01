from dataclasses import dataclass
from conectivos import TokenType, ConectivoLogico

@dataclass(frozen=True)
class Token:
    tipo: TokenType
    valor: str

@dataclass(frozen=True)
class TokenizerResult:
    texto_original: str
    tokens: tuple[Token, ...]

class ErroTokenizer(Exception):
    pass

class FraseInvalida(ErroTokenizer):
    pass

class Tokenizer:
    # Strings brutas para busca no texto
    CONECTIVOS_NOMINAIS = (
        "se e somente se",
        "se",
        "entao",
        "e",
        "ou",
        "nao"
    )

    @classmethod
    def processar(cls, texto: str) -> TokenizerResult:
        palavras = texto.split()
        lista_tokens = []
        acumulo_proposicao = []

        def descarregar_proposicao():
            if acumulo_proposicao:
                conteudo = " ".join(acumulo_proposicao)
                lista_tokens.append(Token(TokenType.PROPOSICAO, conteudo))
                acumulo_proposicao.clear()

        i = 0
        while i < len(palavras):
            match_conectivo = None
            for c in cls.CONECTIVOS_NOMINAIS:
                partes_c = c.split()
                if palavras[i : i + len(partes_c)] == partes_c:
                    match_conectivo = (c, len(partes_c))
                    break

            if match_conectivo:
                descarregar_proposicao()
                lista_tokens.append(Token(TokenType.CONECTIVO, match_conectivo[0]))
                i += match_conectivo[1]
            else:
                acumulo_proposicao.append(palavras[i])
                i += 1
        
        descarregar_proposicao()
        tokens_tupla = tuple(lista_tokens)
        cls._validar_tokens(tokens_tupla)

        return TokenizerResult(texto_original=texto, tokens=tokens_tupla)

    @staticmethod
    def _validar_tokens(tokens: tuple[Token, ...]) -> None:
        if not any(t.tipo == TokenType.PROPOSICAO for t in tokens):
            raise FraseInvalida("A frase deve conter ao menos uma proposição.")
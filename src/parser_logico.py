from dataclasses import dataclass
from tokenizer import TokenizerResult, Token
from conectivos import TokenType, ConectivoLogico

@dataclass(frozen=True)
class Proposicao:
    texto: str
    negada: bool

@dataclass(frozen=True)
class ParserResult:
    proposicoes: tuple[Proposicao, ...]
    conectivo: ConectivoLogico | None

class ErroParser(Exception):
    pass

class EstruturaInvalida(ErroParser):
    pass

class Parser:
    @staticmethod
    def processar(dados_tokenizer: TokenizerResult) -> ParserResult:
        tokens = dados_tokenizer.tokens
        proposicoes_encontradas = []
        conectivo_principal = None
        negacao_ativa = False

        for t in tokens:
            if t.tipo == TokenType.CONECTIVO:
                if t.valor == "nao":
                    negacao_ativa = not negacao_ativa
                    continue

                # Mapeia string do token para o Enum
                if t.valor == "se":
                    conectivo_principal = ConectivoLogico.CONDICIONAL
                elif t.valor == "entao":
                    continue
                elif t.valor == "e":
                    conectivo_principal = ConectivoLogico.E
                elif t.valor == "ou":
                    conectivo_principal = ConectivoLogico.OU
                elif t.valor == "se e somente se":
                    conectivo_principal = ConectivoLogico.BICONDICIONAL
            
            elif t.tipo == TokenType.PROPOSICAO:
                proposicoes_encontradas.append(
                    Proposicao(texto=t.valor, negada=negacao_ativa)
                )
                negacao_ativa = False

        Parser._validar_estrutura(proposicoes_encontradas, conectivo_principal)

        return ParserResult(
            proposicoes=tuple(proposicoes_encontradas),
            conectivo=conectivo_principal
        )

    @staticmethod
    def _validar_estrutura(proposicoes: list[Proposicao], conectivo: ConectivoLogico | None) -> None:
        if not proposicoes:
            raise EstruturaInvalida("Nenhuma proposição encontrada.")
        
        if len(proposicoes) > 1 and not conectivo:
            raise EstruturaInvalida("Múltiplas proposições sem conectivo binário.")
        
        if conectivo and len(proposicoes) < 2:
             raise EstruturaInvalida(f"O operador '{conectivo.value}' exige duas proposições.")

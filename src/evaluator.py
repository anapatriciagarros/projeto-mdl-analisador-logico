from dataclasses import dataclass
from parser_logico import ParserResult, Proposicao
from conectivos import ConectivoLogico, ClassificacaoLogica

@dataclass(frozen=True)
class LinhaTabela:
    entradas: tuple[bool, ...]
    resultado: bool

@dataclass(frozen=True)
class EvaluatorResult:
    formula_original: str
    proposicoes_nomes: tuple[str, ...]
    negacoes: tuple[bool, ...]
    conectivo: ConectivoLogico | None
    tabela: tuple[LinhaTabela, ...]
    classificacao: ClassificacaoLogica

class Evaluator:
    @staticmethod
    def processar(dados_parser: ParserResult, texto_original: str) -> EvaluatorResult:
        nomes_unicos = tuple(p.texto for p in dados_parser.proposicoes)
        num_proposicoes = len(nomes_unicos)
        
        tabela = []
        for i in range(2**num_proposicoes - 1, -1, -1):
            combinacao = tuple(
                bool((i >> j) & 1) for j in range(num_proposicoes - 1, -1, -1)
            )
            
            res = Evaluator._calcular_linha(dados_parser, combinacao)
            tabela.append(LinhaTabela(entradas=combinacao, resultado=res))
        
        tabela_tupla = tuple(tabela)
        
        return EvaluatorResult(
            formula_original=texto_original,
            proposicoes_nomes=nomes_unicos,
            tabela=tabela_tupla,
            negacoes=tuple(p.negada for p in dados_parser.proposicoes),
            conectivo=dados_parser.conectivo,
            classificacao=Evaluator._classificar(tabela_tupla)
        )

    @staticmethod
    def _calcular_linha(dados: ParserResult, combinacao: tuple[bool, ...]) -> bool:
        valores_resolvidos = []
        for i, p in enumerate(dados.proposicoes):
            valor_base = combinacao[i]
            valor_final = not valor_base if p.negada else valor_base
            valores_resolvidos.append(valor_final)

        if len(valores_resolvidos) == 1:
            return valores_resolvidos[0]

        p, q = valores_resolvidos[0], valores_resolvidos[1]
        op = dados.conectivo

        if op == ConectivoLogico.E: return p and q
        if op == ConectivoLogico.OU: return p or q
        if op == ConectivoLogico.CONDICIONAL: return (not p) or q
        if op == ConectivoLogico.BICONDICIONAL: return p == q
        
        return False

    @staticmethod
    def _classificar(tabela: tuple[LinhaTabela, ...]) -> ClassificacaoLogica:
        resultados = [linha.resultado for linha in tabela]
        if all(resultados):
            return ClassificacaoLogica.TAUTOLOGIA
        if not any(resultados):
            return ClassificacaoLogica.CONTRADICAO
        return ClassificacaoLogica.CONTINGENCIA
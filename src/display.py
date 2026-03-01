from tokenizer import TokenizerResult
from evaluator import EvaluatorResult
from conectivos import ClassificacaoLogica, ConectivoLogico

class Display:
    SIMBOLOS = {
        ConectivoLogico.E: "^",
        ConectivoLogico.OU: "v",
        ConectivoLogico.CONDICIONAL: "->",
        ConectivoLogico.BICONDICIONAL: "<->",
        ConectivoLogico.NEGACAO: "~"
    }

    @staticmethod
    def formatar_bool(valor: bool) -> str:
        return "V" if valor else "F"

    @staticmethod
    def exibir_string_original(eval_res: EvaluatorResult) -> None:
        print("\n" + "="*40)
        print(f" SENTENÇA: {eval_res.formula_original.upper()}")
        print("="*40)

    @staticmethod
    def exibir_tokens(tok_res: TokenizerResult) -> None:
        tokens_str = [t.valor for t in tok_res.tokens]
        print(f"\n[Tokens]: {' | '.join(tokens_str)}")

    @staticmethod
    def exibir_proposicoes(eval_res: EvaluatorResult) -> None:
        print("\nPROPOSIÇÕES IDENTIFICADAS:")
        for i, nome in enumerate(eval_res.proposicoes_nomes):
            neg_str = "[NEGADA] " if eval_res.negacoes[i] else ""
            print(f"  P{i+1}: {neg_str}{nome}")

    @staticmethod
    def exibir_mapeamento(eval_res: EvaluatorResult) -> None:
        """Monta a fórmula lógica usando dados estruturados."""
        partes = []
        for i in range(len(eval_res.proposicoes_nomes)):
            simbolo_neg = Display.SIMBOLOS[ConectivoLogico.NEGACAO] if eval_res.negacoes[i] else ""
            partes.append(f"{simbolo_neg}P{i+1}")
        
        print("\nESTRUTURA LÓGICA:")
        if eval_res.conectivo and len(partes) == 2:
            op = Display.SIMBOLOS.get(eval_res.conectivo, "")
            print(f"  Fórmula: {partes[0]} {op} {partes[1]}")
        else:
            print(f"  Fórmula: {partes[0]}")

    @staticmethod
    def exibir_tabela(eval_res: EvaluatorResult) -> None:
        n_props = len(eval_res.proposicoes_nomes)
        
        print("\nTABELA VERDADE:")
        headers = [f"P{i+1}" for i in range(n_props)]
        header_str = " | ".join(headers) + " | RESULTADO"
        print(" " + header_str)
        print("-" * len(header_str))

        for linha in eval_res.tabela:
            entradas_v_f = [Display.formatar_bool(e) for e in linha.entradas]
            res_v_f = Display.formatar_bool(linha.resultado)
            # Alinhamento visual para V e F ficarem sob o P1, P2...
            entradas_str = " | ".join(f" {v} " for v in entradas_v_f)
            print(f" {entradas_str} |     {res_v_f}")

    @staticmethod
    def exibir_classificacao(eval_res: EvaluatorResult) -> None:
        print(f"\nCLASSIFICAÇÃO: {eval_res.classificacao.value}")
        print("="*40 + "\n")

    @classmethod
    def exibir_tudo(cls, tok_res: TokenizerResult, eval_res: EvaluatorResult) -> None:
        cls.exibir_string_original(eval_res)
        cls.exibir_tokens(tok_res)
        cls.exibir_proposicoes(eval_res)
        cls.exibir_mapeamento(eval_res)
        cls.exibir_tabela(eval_res)
        cls.exibir_classificacao(eval_res)
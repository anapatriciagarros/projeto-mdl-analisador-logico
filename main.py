import re

MAX_LEN = 80
ONLY_LETTERS_SPACES = re.compile(r"^[A-Za-z ]+$")  # sem acentos e sem símbolos

def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())

def validar_texto_base(s: str):
    if not s:
        return False, "Frase vazia."
    if len(s) > MAX_LEN:
        return False, f"Frase muito longa (máx {MAX_LEN} caracteres)."
    if not ONLY_LETTERS_SPACES.match(s):
        return False, "Use apenas letras e espaços (sem acentos, números, pontuação ou símbolos)."
    return True, "OK"

def parse_proposicao(texto: str):
    """
    Proposição restrita: 1 ou 2 palavras.
    Pode começar com 'nao ' para negação.
    """
    texto = normalize(texto)
    if texto.startswith("nao "):
        neg = True
        prop = texto[4:].strip()
    else:
        neg = False
        prop = texto

    palavras = prop.split()
    if len(palavras) < 1:
        return None, None, "Proposição vazia."
    if len(palavras) > 2:
        return None, None, "Cada proposição deve ter no máximo 2 palavras (ex.: 'faz frio')."

    return neg, prop, None

def split_frase(frase: str):
    """
    Detecta exatamente 1 conectivo principal.
    Suporta:
      - "se <p> entao <q>"  (implicação)
      - "<p> se e somente se <q>"
      - "<p> ou <q>"
      - "<p> e <q>"
    """
    # 1) Implicação: "se p entao q"
    if frase.startswith("se ") and " entao " in frase:
        partes = frase[3:].split(" entao ")
        if len(partes) != 2:
            return None, None, None, "Frase malformada com 'se ... entao'."
        return partes[0].strip(), "se entao", partes[1].strip(), None

    # 2) Bicondicional (precisa vir antes de 'e', porque contém 'e')
    if " se e somente se " in frase:
        partes = frase.split(" se e somente se ")
        if len(partes) != 2:
            return None, None, None, "Frase malformada com 'se e somente se'."
        return partes[0].strip(), "se e somente se", partes[1].strip(), None

    # 3) OU
    if " ou " in frase:
        partes = frase.split(" ou ")
        if len(partes) != 2:
            return None, None, None, "Use apenas UM 'ou' na frase."
        return partes[0].strip(), "ou", partes[1].strip(), None

    # 4) E
    if " e " in frase:
        partes = frase.split(" e ")
        if len(partes) != 2:
            return None, None, None, "Use apenas UM 'e' na frase."
        return partes[0].strip(), "e", partes[1].strip(), None

    return None, None, None, "Nao encontrei conectivo. Use: e / ou / se ... entao / se e somente se."

def eval_formula(p_base: bool, q_base: bool, neg_p: bool, neg_q: bool, conectivo: str) -> bool:
    p = (not p_base) if neg_p else p_base
    q = (not q_base) if neg_q else q_base

    if conectivo == "e":
        return p and q
    if conectivo == "ou":
        return p or q
    if conectivo == "se entao":   # p -> q
        return (not p) or q
    if conectivo == "se e somente se":  # p <-> q
        return p == q
    raise ValueError("Conectivo inválido.")

def imprimir_tokens(frase: str, conectivo: str):
    """
    Saída extra para cumprir o 'mapeamento de conectivos' do professor.
    """
    mapa = {
        "e": "∧",
        "ou": "∨",
        "se entao": "→",
        "se e somente se": "↔",
        "nao": "¬"
    }

    # tokenização simples por palavras
    palavras = frase.split()

    tokens = []
    i = 0
    while i < len(palavras):
        # detecta "se e somente se"
        if i + 3 < len(palavras) and palavras[i:i+4] == ["se", "e", "somente", "se"]:
            tokens.append(mapa["se e somente se"])
            i += 4
            continue
        # detecta "entao" (parte do "se ... entao")
        if palavras[i] == "entao":
            tokens.append("entao")
            i += 1
            continue
        if palavras[i] == "se":
            tokens.append("se")
            i += 1
            continue
        if palavras[i] == "nao":
            tokens.append(mapa["nao"])
            i += 1
            continue
        if palavras[i] == "e":
            tokens.append(mapa["e"])
            i += 1
            continue
        if palavras[i] == "ou":
            tokens.append(mapa["ou"])
            i += 1
            continue

        # resto vira "texto" (parte da proposição)
        tokens.append(palavras[i])
        i += 1

    # pós-processamento: se conectivo for "se entao", imprime como →
    if conectivo == "se entao":
        # só para exibir bonitinho: troca sequência "se ... entao" por "→" na visão lógica
        # (sem bagunçar muito, só mostra o mapeamento)
        pass

    print("\n============= String Tokenizada: =============")
    for t in tokens:
        print(f"Token: {t}")

def imprimir_tabela(neg_p: bool, neg_q: bool, conectivo: str):
    sym = {"e": "∧", "ou": "∨", "se entao": "→", "se e somente se": "↔"}[conectivo]
    cab_p = "¬p" if neg_p else "p"
    cab_q = "¬q" if neg_q else "q"
    formula = f"{cab_p} {sym} {cab_q}"

    print("\n--- Tabela Verdade ---")
    print(f" p | q | {cab_p:^3} | {cab_q:^3} | {formula}")
    print("-" * (18 + len(formula)))

    comb = [(True, True), (True, False), (False, True), (False, False)]
    resultados = []

    def VF(x): return "V" if x else "F"

    for pb, qb in comb:
        res = eval_formula(pb, qb, neg_p, neg_q, conectivo)
        resultados.append(res)
        pr = (not pb) if neg_p else pb
        qr = (not qb) if neg_q else qb
        print(f" {VF(pb)} | {VF(qb)} | {VF(pr):^3} | {VF(qr):^3} | {VF(res):^{len(formula)}}")

    if all(resultados):
        cls = "TAUTOLOGIA"
    elif not any(resultados):
        cls = "CONTRADIÇÃO"
    else:
        cls = "CONTINGÊNCIA"
    print(f"\nClassificação: {cls}\n")

def main():
    print("=== Analisador Lógico (Restrito a 2 proposições) ===")
    print("REGRAS (Entrada Restrita):")
    print("  - Formatos aceitos:")
    print("      [nao] prop1 e [nao] prop2")
    print("      [nao] prop1 ou [nao] prop2")
    print("      se [nao] prop1 entao [nao] prop2")
    print("      [nao] prop1 se e somente se [nao] prop2")
    print("  - Cada proposição: 1 ou 2 palavras (ex.: 'chove', 'faz frio')")
    print("  - Sem acentos e sem pontuação.")
    print("  - Digite 'sair' para encerrar.\n")

    print("Exemplos:")
    print("  chove e faz frio")
    print("  nao esta sol ou fica quente")
    print("  se estudo entao tiro nota")
    print("  trabalho se e somente se estudo\n")

    while True:
        frase = input("Digite a frase: ").strip()
        if frase.lower().strip() == "sair":
            print("Encerrado.")
            break

        frase = normalize(frase)
        ok, msg = validar_texto_base(frase)
        if not ok:
            print(f"\nNÃO RECONHECIDO: {msg}\n")
            continue

        p_raw, conectivo, q_raw, err = split_frase(frase)
        if err:
            print(f"\nNÃO RECONHECIDO: {err}\n")
            continue

        neg_p, p_pura, errp = parse_proposicao(p_raw)
        if errp:
            print(f"\nNÃO RECONHECIDO: problema em p: {errp}\n")
            continue

        neg_q, q_pura, errq = parse_proposicao(q_raw)
        if errq:
            print(f"\nNÃO RECONHECIDO: problema em q: {errq}\n")
            continue

        if p_pura == q_pura:
            print("\nNÃO RECONHECIDO: p e q precisam ser proposições DIFERENTES.\n")
            continue

        # Saídas exigidas (identificação + mapeamento + tabela)
        sym = {"e": "∧", "ou": "∨", "se entao": "→", "se e somente se": "↔"}[conectivo]
        sentenca = f"{'¬p' if neg_p else 'p'} {sym} {'¬q' if neg_q else 'q'}"

        print("\n============= String Original: =============")
        print(frase)

        imprimir_tokens(frase, conectivo)

        print("\n============= Proposições Identificadas: =============")
        print(f"p: {p_pura}")
        print(f"q: {q_pura}")

        print("\n============= Mapeamento Lógico: =============")
        print(f"Sentença lógica: {sentenca}")

        imprimir_tabela(neg_p, neg_q, conectivo)

if __name__ == "__main__":
    main()

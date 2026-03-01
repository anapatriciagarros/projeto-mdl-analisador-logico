import re
from dataclasses import dataclass

MAX_LEN = 80
# Aceita letras acentuadas, cedilha e espaços
ONLY_LETTERS_SPACES = re.compile(r"^[a-záàâãéèêíïóôõöúç ]+$")

PRONOMES_IGNORADOS = {"eu", "tu", "ele", "ela", "nos", "nós", "vos", "vós", "eles", "elas"}

class ErroPreprocessor(Exception):
    pass

class TextoVazio(ErroPreprocessor):
    pass

class TextoLongo(ErroPreprocessor):
    pass

class CaracteresInvalidos(ErroPreprocessor):
    pass

@dataclass(frozen=True)
class PreprocessingResult:
    entrada_bruta: str
    texto_normalizado: str

class Preprocessor:
    def __init__(self, entrada: str):
        self.entrada_bruta = entrada
        self._texto = ""

    def _normalize(self) -> None:
        self._texto = " ".join(self.entrada_bruta.strip().lower().split())

    def _remover_pronomes(self) -> None:
        palavras = [p for p in self._texto.split() if p not in PRONOMES_IGNORADOS]
        self._texto = " ".join(palavras)

    def _validar(self) -> None:
        if not self._texto:
            raise TextoVazio("Frase vazia após normalização.")

        if len(self._texto) > MAX_LEN:
            raise TextoLongo(f"Frase muito longa (máx {MAX_LEN} caracteres).")

        if not ONLY_LETTERS_SPACES.match(self._texto):
            raise CaracteresInvalidos("Use apenas letras e espaços.")

    def processar(self) -> PreprocessingResult:
        self._normalize()
        self._remover_pronomes()
        self._validar()
        return PreprocessingResult(
            entrada_bruta=self.entrada_bruta,
            texto_normalizado=self._texto
        )
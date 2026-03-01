import sys
from preprocessor import Preprocessor, ErroPreprocessor
from tokenizer import Tokenizer, ErroTokenizer
from parser_logico import Parser, ErroParser
from evaluator import Evaluator
from display import Display

def executar_pipeline(entrada_usuario: str):
    try:
        pre_res = Preprocessor(entrada_usuario).processar()

        tok_res = Tokenizer.processar(pre_res.texto_normalizado)

        par_res = Parser.processar(tok_res)

        eval_res = Evaluator.processar(par_res, pre_res.texto_normalizado)

        Display.exibir_tudo(tok_res, eval_res)

    except ErroPreprocessor as e:
        print(f"\n[ERRO DE ENTRADA]: {e}")
    except ErroTokenizer as e:
        print(f"\n[ERRO DE TOKENIZAÇÃO]: {e}")
    except ErroParser as e:
        print(f"\n[ERRO DE ESTRUTURA]: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")

def main():
    print("=== SISTEMA DE ANÁLISE PROPOSICIONAL ===")
    print("Exemplos: ")
    print("  - se eu estudo entao eu passo")
    print("  - hoje chove e faz frio")
    print("  - nao esta sol se e somente se nuvens aparecem")
    print("-" * 40)

    while True:
        try:
            entrada = input("\nDigite uma proposição (ou 'sair'): ").strip()
            
            if entrada.lower() in ('sair', 'exit', 'q'):
                print("Encerrando...")
                break
                
            if not entrada:
                continue

            executar_pipeline(entrada)

        except KeyboardInterrupt:
            print("\nEncerrando...")
            break

if __name__ == "__main__":
    main()
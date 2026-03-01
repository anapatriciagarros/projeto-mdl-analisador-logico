# Analisador de Sentenças Lógicas Proposicionais com Geração Automática de Tabela-Verdade

## Objetivo do Projeto

Este sistema foi desenvolvido como parte da **Atividade 2** da disciplina de Lógica e Matemática Discreta. O objetivo é unir a fundamentação teórica da lógica formal com competências de programação, automatizando a análise de proposições e a geração de tabelas-verdade.

O programa recebe sentenças em linguagem natural controlada, identifica componentes lógicos e gera uma saída visual clara da estrutura da fórmula e sua classificação.

---

## Fundamentação Teórica

O projeto implementa os conceitos de **Lógica Proposicional**, processando os seguintes conectivos:

| Conectivo Lógico | Símbolo | Representação no Código |
| --- | --- | --- |
| **Negação** | $\neg$ | `nao` |
| **Conjunção** | $\wedge$ | `e` |
| **Disjunção** | $\vee$ | `ou` |
| **Condicional** | $\rightarrow$ | `se ... entao` |
| **Bicondicional** | $\leftrightarrow$ | `se e somente se` |

### Classificação da Tabela-Verdade:

1. **Tautologia:** Quando todos os resultados da tabela são Verdadeiros ($V$).
2. **Contradição:** Quando todos os resultados são Falsos ($F$).
3. **Contingência:** Quando há resultados $V$ e $F$ misturados.

---

## Requisitos Técnicos e Implementação

### 1. Entrada Restrita (Input Validation)

Para evitar a ambiguidade da língua natural, o sistema utiliza **Expressões Regulares (Regex)** para validar o texto.

* Limite de 80 caracteres.
* Proposições atômicas limitadas a 2 palavras (ex: "faz sol").
* Bloqueio de caracteres especiais e números para garantir a integridade da análise lógica.
* O sistema ignora pronomes pessoais (eu, tu, ele, nós, etc.) para focar no núcleo da proposição (ex: "eu estudo" torna-se apenas "estudo").

### 2. Processamento (Tokenização)

O sistema realiza o mapeamento dos conectivos e separa as proposições $p$ e $q$. O motor de avaliação (`eval_formula`) utiliza álgebra booleana para calcular os resultados de cada linha da tabela $2^n$ (onde $n=2$ neste projeto).

### 3. Saída Visual

A tabela-verdade é exibida no console com formatação de colunas, facilitando a leitura da relação entre as entradas e o resultado final da expressão lógica.

---

## Como Executar o Projeto

1. **Pré-requisitos:** Ter o Python 3.x instalado.
2. **Clonar o Repositório:**
```bash
git clone https://github.com/anapatriciagarros/projeto-mdl-analisador-logico.git

```


3. **Executar o Script:**
```bash
python main.py

```



## Exemplo de Execução

Para ilustrar o funcionamento do sistema, abaixo apresentamos uma simulação real de uso com uma sentença condicional.

### Entrada do Usuário:

> `se como entao fico cheia`

### Processamento e Saída:

1. **Tokenização:** O sistema quebra a frase em unidades lógicas, identificando palavras-chave e conectivos.
2. **Identificação de Proposições:** São extraídas as proposições atômicas $p$ e $q$.
3. **Mapeamento Lógico:** A frase é convertida para a notação formal da lógica de predicados.
4. **Tabela-Verdade:** O sistema calcula todas as combinações de valores lógicos ($V/F$).

#### Demonstração no Console:

```text
============= String Original: =============
se como entao fico cheia

============= String Tokenizada: =============
Token: se
Token: como
Token: entao
Token: fico
Token: cheia

============= Proposições Identificadas: =============
p: como
q: fico cheia

============= Mapeamento Lógico: =============
Sentença lógica: p → q

--- Tabela Verdade ---
 p | q |  p  |  q  | p → q
-----------------------
 V | V |  V  |  V  |   V
 V | F |  V  |  F  |   F
 F | V |  F  |  V  |   V
 F | F |  F  |  F  |   V

Classificação: CONTINGÊNCIA

```

### Explicação do Resultado

* **Análise Lógica:** A sentença foi identificada como uma **Condicional** ($p \to q$). Na lógica formal, uma condicional só é falsa quando a premissa ($p$) é verdadeira e a conclusão ($q$) é falsa (linha 2 da tabela).  
* **Classificação:** Como o resultado final apresenta tanto valores Verdadeiros quanto Falsos dependendo da entrada, a sentença é classificada tecnicamente como uma **Contingência**.  

---



## Integrantes (Grupo)

* **Ana Patricia Garros Viegas** - 2022003512  
* **Ana Poliana Mesquita de Jesus de Sousa** - 20250013597  
* **Marcos Vinicius Jansem Oliveira** - 20250071278  
* **Maria Laura Rangel Urbano Cronemberger** - 20250071287  
* **Tiago de Lima Batista** - 20250013739    
* **Wesley dos Santos Gatinho** - 20250071367  

---

## Informações da Disciplina

**Disciplina:** EECP0015 — Lógica e Matemática Discreta    
**Professor:** Prof. Rondineli Seba  
**Instituição:** UFMA — Universidade Federal do Maranhão  
**Semestre:** 2025.4  

---
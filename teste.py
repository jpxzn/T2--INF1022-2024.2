import ply.lex as lex
import ply.yacc as yacc

# Definição dos tokens
tokens = (
    'FACA', 'MOSTRE', 'SER', 'NUM', 'VAR', 'PONTO', 'MAIS'
)

# Definições dos tokens para palavras-chave (em maiúsculas)
t_FACA = r'FACA'
t_MOSTRE = r'MOSTRE'
t_SER = r'SER'
t_PONTO = r'\.'
t_MAIS = r'MAIS'

# Definição do token VAR (variáveis, que começam com letra e podem ter números ou letras)
def t_VAR(t):
    r'[a-z][a-zA-Z0-9]*'  # A variável deve começar com uma letra minúscula
    return t

# Definição para números (valores inteiros)
def t_NUM(t):
    r'\d+'  # Um ou mais dígitos
    t.value = int(t.value)  # Converte para inteiro
    return t

# Ignorar espaços em branco
t_ignore = ' \t'

# Regras para tratar novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Função de erro (caso encontre caracteres inválidos)
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()

# Funções do parser para manipulação dos comandos
def p_programa(p):
    '''programa : cmds'''
    p[0] = p[1]

def p_cmds(p):
    '''cmds : cmd cmds
            | cmd'''
    p[0] = [p[1]] + (p[2] if len(p) > 2 else [])

def p_cmd_atribuicao(p):
    '''cmd : FACA VAR SER NUM PONTO'''
    p[0] = f"{p[2]} = {p[4]}"  # Atribuição em Python

def p_cmd_impressao(p):
    '''cmd : MOSTRE VAR PONTO'''
    p[0] = f"print({p[2]})"  # Gera código Python para imprimir a variável

def p_cmd_soma(p):
    '''cmd : FACA VAR SER VAR MAIS VAR PONTO'''
    p[0] = f"{p[2]} = {p[4]} + {p[6]}"  # Atribuição com soma

def p_error(p):
    print(f"Erro de sintaxe: {p}")

# Criar o parser
parser = yacc.yacc()

# Tabela de símbolos para armazenar as palavras e suas contagens
TS = {}

# Função para adicionar uma palavra à tabela de símbolos
def coloca_palavra_na_TS(palavra):
    if isinstance(palavra, str):  # Verifica se é uma string (palavra)
        palavra = palavra.lower()  # Converte a palavra para minúsculas
        if palavra in TS:
            TS[palavra] += 1
        else:
            TS[palavra] = 1
    else:
        # Se for número, não fazemos a conversão para minúsculas
        TS[palavra] = 1  # Adiciona número na tabela de símbolos sem alterações

def main():
    dado = """
    FACA x SER 5.
    FACA y SER 10.
    FACA z SER x MAIS y.
    MOSTRE z.
    """
    lexer.input(dado)
    while True:
        tok = lexer.token()
        if not tok:
            break
        coloca_palavra_na_TS(tok.value)

    # Exibe a tabela de símbolos
    print("Tabela de Símbolos:")
    for palavra, ocur in TS.items():
        print(f"{palavra}: {ocur}")

    # Processa a entrada com o parser
    resultado = parser.parse(dado)
    if resultado:
        print("\nCódigo gerado:")
        generated_code = "\n".join(resultado)  # Código gerado em Python
        
        # Escrever o código gerado em um arquivo 'out.py'
        with open('out.py', 'w') as file:
            file.write(generated_code)
        
        print(generated_code)
    else:
        print("Erro ao parsear o código.")

if __name__ == "__main__":
    main()

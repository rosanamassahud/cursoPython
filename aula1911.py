# Leitura e escrita em arquivos de texto (txt)
'''
    O que é um arquivo TXT?
    É um arquivo simples que contém texto puro.
    Permite salvar informações para usar depois → persistência de dados.

    ✔ Função open()

    open(nome, modo)

    Modos mais usados:

    "w" → escreve (apaga o conteúdo anterior)
    "a" → adiciona ao final (append)
    "r" → lê o arquivo
'''

#Exemplo 1 — Criar e escrever (modo w)
with open("dados.txt", "w", encoding="utf-8") as f:
    f.write("Primeira linha\n")
    f.write("Segunda linha\n")

'''
Explicação:

with fecha o arquivo automaticamente

\n pula linha
'''

#Exemplo 2 — Adicionar conteúdo (modo a)
#with open("dados.txt", "a", encoding="utf-8") as f:
#    f.write("Linha adicionada depois\n")

#3. Lendo arquivos (modo r)
#Exemplo 3 — Ler tudo de uma vez

#with open("dados.txt", "r", encoding="utf-8") as f:
#    texto = f.read()

#print(texto)

#Exemplo 4 — Ler linha por linha
#with open("dados.txt", "r", encoding="utf-8") as f:
#    for linha in f:
#        print("Linha:", linha.strip())

'''
Explicação:
O strip() remove o \n.
'''

#Trabalhando com listas e arquivos - exemplo prático
#Exemplo 5 — Salvar uma lista no arquivo
#nomes = ["Ana", "Pedro", "Marcos"]

#with open("nomes.txt", "w", encoding="utf-8") as f:
#    for nome in nomes:
#        f.write(nome + "\n")

# Exemplo 6 — Ler o arquivo e transformar em lista
#lista = []

#with open("nomes.txt", "r", encoding="utf-8") as f:
#    for linha in f:
#        lista.append(linha.strip())

#print(lista)
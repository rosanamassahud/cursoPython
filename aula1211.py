# estudo sobre listas em Python

# para criar uma lista
lista_vazia = []
# ou
lista_vazia_2 = list()

#para criar uma lista  com valores
lista_numeros = [3,9,10, 3.5, 89,23,18,1,45]
lista_nomes = ['Kiko', 'José', 'Ana', 'Maria', 'João']
lista_misturada = ['mesa', 1, 9.8,'Pulguinha']

#impimir listas. Basta fazer um print com a lista
print(lista_numeros)
print('Lista de nomes: {}'.format(lista_nomes))
print('Lista misturada:', lista_misturada)

print('Imprimir os elementos da lista_numeros 1 a 1:')
#imprimir os elementos de uma lista 1 a 1
for item in lista_numeros:
    print(item)

# anexar elementos em uma lista
# append adiciona o elemento no final da lista
print('Inserir elemento na lista_nomes:')
lista_nomes.append('Jaiminho')
print(lista_nomes)

# acessar o elemento de uma posição específica
# obs.: a indexação começa sempre do 0 (zero)
print('lista_numeros[2]:', lista_numeros[2])
print()

# modificar um elemento
# basta acessar o elemento indicando a posição e indicar o novo valor
print('Lista misturada antes de modificar:', lista_misturada)
print('Modificar o elem. lista_misturada[3]')
lista_misturada[3] = 20
print('Lista misturada depois de modificar:', lista_misturada)

# ordenando listas
print('Listas antes da ordenação')
print('Lista de números:',lista_numeros)
print('Lista de nomes:',lista_nomes)

lista_numeros.sort()
lista_nomes.sort()

print('Listas depois da ordenação')
print('Lista de números:',lista_numeros)
print('Lista de nomes:',lista_nomes)

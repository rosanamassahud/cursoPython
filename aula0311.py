'''
idade = int(input('Digite a sua idade: '))
nome = input('Digite seu nome: ')
print('Boa tarde, {}. Você tem {} anos'.format(nome, idade))

if (idade >= 18):
    print('Você é maior de idade.')
    print('Você já pode tirar carteira.')
    print('Você é obrigado a votar.')
else:
    print('Você é menor de idade')

if (idade >= 18 and idade < 70):
    print('Você é obrigado a votar.')
elif((idade >= 16 and idade < 18) or (idade >= 70)):
    print('Você é um eleitor facultativo')
else:
    print('Você é não eleitor.')
'''

numero = int(input('Digite um número: '))
resto = numero % 2

if(resto == 0):
    print('O número é par')
else:
    print('O número é ímpar')
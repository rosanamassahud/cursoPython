import random
import time

def apres_adivinhacao():
    print('------------------------------------------------')
    print('------- Bem vindo ao jogo de adivinhação -------')
    print('------------------------------------------------')

def imprime_pontos(jogador, pontos):
    print('------------------------------------------------')
    print('Jogador: {}\nPontos: {}'.format(jogador,pontos))
    print('------------------------------------------------')

def gera_numero_secreto():
    random.seed(time.time())
    numero_secreto = random.randint(0, 100)
    #print(numero_secreto)
    return numero_secreto

def define_nivel():
    print('----- Nível do jogo -----')
    print('1-Fácil \n2-Médio\n3-Difícil')
    nivel = int(input('Escolha o nível: '))
    return nivel

def define_jogador():
    jogador = input('Qual o seu nome? ')
    return jogador

def configura_jogo():
    numero_secreto = gera_numero_secreto()
    nivel = define_nivel()
    numero_tentativas = 0
    if(nivel == 1):
        numero_tentativas = 20
    elif(nivel == 2):
        numero_tentativas = 10
    else:
        numero_tentativas = 5
    return numero_secreto, numero_tentativas

def menu():
    print()
    print('1-Jogar')
    print('0-Sair do programa')
    op = int(input('O que deseja fazer agora? '))
    return op

def jogar(jogador):
    numero_secreto, numero_tentativas = configura_jogo()
    tentativa = 1
    pontos = 1000
    while(tentativa <= numero_tentativas): 

        chute = int(input('Adivinha o número (inteiro): '))

        # teste do chute
        if (chute == numero_secreto):
            print('Você acertou!')
            print('Parabéns!')
            break
        else:
            print('Você errou!')    
            pontos = pontos - float((abs(numero_secreto-chute))/2)
            if (chute > numero_secreto):
                print('Você chutou um número MAIOR que o número secreto')
            elif (chute < numero_secreto):
                print('Você chutou um número MENOR que o número secreto')
            print('Tente novamente')
        tentativa = tentativa + 1
        imprime_pontos(jogador, pontos)
    imprime_pontos(jogador, pontos)
    print('Fim do jogo')

apres_adivinhacao()
jogador = define_jogador()
opcao = menu()
while(opcao == 1):
    jogar(jogador)
    opcao = menu()
else:
    print('Encerrando o jogo.')
    print('Saindo do programa...')

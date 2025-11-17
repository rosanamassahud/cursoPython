# Jogo: Caça ao Tesouro

import random

# cria uma lista de 10 posições vazias
trilha = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]

# escolhe aleatoriamente uma posição para esconder o tesouro
pos_tesouro = random.randint(0, len(trilha) - 1)

tentativas = 0

print("=== JOGO: CAÇA AO TESOURO ===")
print("A trilha tem 6 posições: 0, 1, 2, 3, 4, 5, 6, 7, 8 e 9.")
print("Tente encontrar o tesouro!\n")

while (True):
    palpite = int(input("Escolha uma posição (0 a 9): "))
    tentativas += 1

    # verifica se o palpite está correto
    if (palpite == pos_tesouro):
        print("\n💎 Parabéns! Você encontrou o tesouro!")
        print(f"Foram necessárias {tentativas} tentativas.")
        break
    else:
        print("Nada aqui! Tente outra posição...\n")

import tkinter as tk
import random

# Escolhe a posição do tesouro (0 a 5)
pos_tesouro = random.randint(0, 5)

# Função chamada quando o usuário clica em um botão
def tentar(posicao):
    if (posicao == pos_tesouro):
        botao_list[posicao].config(text="💎 Tesouro!", bg="lightgreen")
        resultado_label.config(text="Parabéns! Você encontrou o tesouro!")
        
        # Desativar todos os botões após vencer
        for b in botao_list:
            b.config(state="disabled")
    else:
        botao_list[posicao].config(text="X", bg="lightcoral", state="disabled")
        resultado_label.config(text="Nada aqui... continue procurando!")

# Janela principal
janela = tk.Tk()
janela.title("Caça ao Tesouro")

titulo = tk.Label(janela, text="Clique em uma posição para procurar o tesouro!", font=("Arial", 12))
titulo.pack(pady=10)

# Frame para organizar os botões da trilha
frame = tk.Frame(janela)
frame.pack()

botao_list = []

# Criar 6 botões (posições da trilha)
for i in range(6):
    botao = tk.Button(frame, text=f"{i}", width=10, height=2,
                      command=lambda pos=i: tentar(pos))
    botao.grid(row=0, column=i, padx=5, pady=5)
    botao_list.append(botao)

resultado_label = tk.Label(janela, text="", font=("Arial", 12))
resultado_label.pack(pady=10)

janela.mainloop()

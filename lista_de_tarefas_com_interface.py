# To-do (lista de tarefas)

import tkinter as tk

def adicionar():
    tarefa = entrada.get()
    if (tarefa):
        lista.insert(tk.END, tarefa)
        entrada.delete(0, tk.END)

def remover():
    try:
        indice = lista.curselection()[0]
        lista.delete(indice)
    except:
        pass


janela = tk.Tk()
janela.title("Lista de Tarefas")

entrada = tk.Entry(janela, width=30)
entrada.pack()

botao_add = tk.Button(janela, text="Adicionar", command=adicionar)
botao_add.pack()

lista = tk.Listbox(janela, width=40)
lista.pack()

botao_remover = tk.Button(janela, text="Remover Selecionada", command=remover)
botao_remover.pack()

janela.mainloop()

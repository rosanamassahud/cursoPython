import tkinter as tk
from tkinter import messagebox
import os

ARQUIVO = "tarefas.txt"

# ---------------------------
# Funções de Persistência
# ---------------------------

def carregar_tarefas():
    """Lê o arquivo e carrega as tarefas na Listbox"""
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            for linha in f:
                tarefa = linha.strip()
                if tarefa:
                    lista.insert(tk.END, tarefa)

def salvar_tarefas():
    """Salva todas as tarefas atuais no arquivo"""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for i in range(lista.size()):
            f.write(lista.get(i) + "\n")

# ---------------------------
# Funções da Interface
# ---------------------------

def adicionar_tarefa():
    tarefa = entrada.get().strip()
    if tarefa:
        lista.insert(tk.END, tarefa)
        entrada.delete(0, tk.END)
        salvar_tarefas()  # Salva ao adicionar
    else:
        messagebox.showwarning("Aviso", "Digite uma tarefa!")

def remover_tarefa():
    try:
        indice = lista.curselection()[0]
        lista.delete(indice)
        salvar_tarefas()  # Salva ao remover
    except:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

# ---------------------------
# Interface Tkinter
# ---------------------------

janela = tk.Tk()
janela.title("Lista de Tarefas")
janela.geometry("300x350")

# Entrada
entrada = tk.Entry(janela, width=25)
entrada.pack(pady=10)

# Botões
btn_add = tk.Button(janela, text="Adicionar", width=20, command=adicionar_tarefa)
btn_add.pack()

btn_remove = tk.Button(janela, text="Remover", width=20, command=remover_tarefa)
btn_remove.pack(pady=5)

# Lista de tarefas
lista = tk.Listbox(janela, width=30, height=12)
lista.pack(pady=10)

# Carregar tarefas ao iniciar
carregar_tarefas()

janela.mainloop()

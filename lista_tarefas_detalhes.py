import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

ARQUIVO = "tarefas.csv"
CAMPOS = ["tarefa", "status", "data_criacao", "data_conclusao"]

# ---------------------------
# Persistência em CSV
# ---------------------------

def carregar_tarefas():
    """Lê o CSV e carrega na Listbox"""
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CAMPOS)
            writer.writeheader()
        return

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            texto = formatar_exibicao(linha)
            lista.insert(tk.END, texto)

def salvar_tarefas(dados):
    """Salva toda a lista no CSV"""
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)

def ler_tarefas():
    """Retorna uma lista de dicionários com os registros do CSV"""
    tarefas = []
    if not os.path.exists(ARQUIVO):
        return tarefas

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for linha in reader:
            tarefas.append(linha)
    return tarefas

def formatar_exibicao(linha):
    """Formata como aparece na Listbox"""
    return f"{linha['tarefa']}  |  {linha['status']}"

# ---------------------------
# Funções da Interface
# ---------------------------

def adicionar_tarefa():
    tarefa = entrada.get().strip()
    if not tarefa:
        messagebox.showwarning("Aviso", "Digite uma tarefa!")
        return

    nova_linha = {
        "tarefa": tarefa,
        "status": "Pendente",
        "data_criacao": datetime.now().strftime("%Y-%m-%d"),
        "data_conclusao": ""
    }

    tarefas = ler_tarefas()
    tarefas.append(nova_linha)
    salvar_tarefas(tarefas)

    lista.insert(tk.END, formatar_exibicao(nova_linha))
    entrada.delete(0, tk.END)

def remover_tarefa():
    try:
        indice = lista.curselection()[0]
    except:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")
        return

    tarefas = ler_tarefas()
    tarefas.pop(indice)
    salvar_tarefas(tarefas)

    lista.delete(indice)

def concluir_tarefa():
    try:
        indice = lista.curselection()[0]
    except:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para concluir!")
        return

    tarefas = ler_tarefas()
    tarefas[indice]["status"] = "Concluída"
    tarefas[indice]["data_conclusao"] = datetime.now().strftime("%Y-%m-%d")

    salvar_tarefas(tarefas)

    lista.delete(indice)
    lista.insert(indice, formatar_exibicao(tarefas[indice]))

# ---------------------------
# Interface Gráfica Tkinter
# ---------------------------

janela = tk.Tk()
janela.title("Lista de Tarefas (CSV)")
janela.geometry("380x420")

# Entrada
entrada = tk.Entry(janela, width=30)
entrada.pack(pady=10)

# Botões
btn_add = tk.Button(janela, text="Adicionar", width=25, command=adicionar_tarefa)
btn_add.pack()

btn_done = tk.Button(janela, text="Marcar como concluída", width=25, command=concluir_tarefa)
btn_done.pack(pady=5)

btn_remove = tk.Button(janela, text="Remover", width=25, command=remover_tarefa)
btn_remove.pack()

# Lista de tarefas
lista = tk.Listbox(janela, width=45, height=15)
lista.pack(pady=10)

# Carregar dados ao iniciar
carregar_tarefas()

janela.mainloop()

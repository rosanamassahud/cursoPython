# Programa: Lista de Tarefas (To-do)

tarefas = []  # lista vazia para armazenar as tarefas

while (True):
    print("\n=== LISTA DE TAREFAS ===")
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("3 - Remover tarefa")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if (opcao == "1"):
        tarefa = input("Digite a nova tarefa: ")
        tarefas.append(tarefa)
        print("Tarefa adicionada!")

    elif (opcao == "2"):
        if (not tarefas):
            print("Nenhuma tarefa cadastrada.")
        else:
            print("\nTarefas:")
            for i, t in enumerate(tarefas):
                print(f"{i+1} - {t}")

    elif (opcao == "3"):
        if (not tarefas):
            print("Nenhuma tarefa para remover.")
        else:
            indice = int(input("Informe o número da tarefa a remover: "))-1
            if (0 <= indice < len(tarefas)):
                removida = tarefas.pop(indice)
                print(f"Tarefa removida: {removida}")
            else:
                print("Índice inválido!")

    elif (opcao == "0"):
        print("Saindo... Até mais!")
        break

    else:
        print("Opção inválida!")

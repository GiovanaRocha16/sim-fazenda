
def fabricar(fazenda):
    if fazenda.nivel < 3:
        print("🏭 Fábrica desbloqueia apenas no nível 3!", "vermelho")
        return

    if not fazenda.gastar_energia(1):
        return  

    print("\n--- FÁBRICA ---")
    print("1. 🧀 Queijo (2 Leites)")
    print("2. 🧈 Manteiga (3 Leites)")
    print("3. 🧶 Suéter (3 Lãs)")
    if fazenda.nivel >= 4:
        print("4. 🍣 Sushi (1 Peixe Comum 🐟 + 1 Arroz 🌾)")

    escolha = input("Escolha o produto para fabricar: ")

    def remover_itens(nome, quantidade):
        count = 0
        for item in fazenda.estoque[:]:
            if item["nome"] == nome and count < quantidade:
                fazenda.estoque.remove(item)
                if nome in fazenda.status_estoque:
                    fazenda.status_estoque.remove(nome)
                count += 1
        return count == quantidade

    if escolha == "1":
        if remover_itens("Leite", 2):
            fazenda.estoque.append({"nome": "Queijo", "preco": 25})
            fazenda.status_estoque.append("Queijo")
            print("🧀 Queijo produzido com sucesso!")
            fazenda.ganhar_xp(10)
        else:
            print("❌ Não há leites suficientes.")

    elif escolha == "2":
        if remover_itens("Leite", 3):
            fazenda.estoque.append({"nome": "Manteiga", "preco": 40})
            fazenda.status_estoque.append("Manteiga")
            print("🧈 Manteiga produzida com sucesso!")
            fazenda.ganhar_xp(15)
        else:
            print("❌ Não há leites suficientes.")

    elif escolha == "3":
        if remover_itens("Lã", 3):
            fazenda.estoque.append({"nome": "Suéter", "preco": 60})
            fazenda.status_estoque.append("Suéter")
            print("🧶 Suéter produzido com sucesso!")
            fazenda.ganhar_xp(20)
        else:
            print("❌ Não há lãs suficientes.")

    elif escolha == "4" and fazenda.nivel >= 4:
        if remover_itens("Peixe Comum", 1) and remover_itens("Arroz", 1):
            fazenda.estoque.append({"nome": "Sushi 🍣", "preco": 35})
            fazenda.status_estoque.append("Sushi")
            print("🍣 Sushi produzido com sucesso!")
            fazenda.ganhar_xp(25)
        else:
            print("❌ Ingredientes insuficientes para fazer Sushi.")

    else:
        print("Opção inválida. Voltando ao menu principal...")

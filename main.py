from package.fazenda import Fazenda
from escolher_animal_ou_planta import escolher_animal_ou_planta
from package.fabrica import fabricar
from package.lagoa_dos_peixes import lagoa_dos_peixes
from utils import colorir 

def main():
    print(colorir("🌾 Bem-vindo ao Sim fazenda! 🌾", "verde" ))
    nome_fazenda = input("Digite o nome da sua fazenda: ")
    fazenda = Fazenda(nome_fazenda)

    while True:
        opcao_fabrica = fazenda.nivel >= 3
        opcao_lagoa = fazenda.nivel >= 4

        print(f"\n🏡 {fazenda.nome} - Dia {fazenda.dia} 🌤️ | Nível ✨: {fazenda.nivel} | Dinheiro 💰: {fazenda.dinheiro} | Energia ⚡: {fazenda.energia}/{fazenda.energia_max}")
        print(colorir("1. Ir ao mercadinho", "amarelo"))
        print(colorir("2. Comprar Animal ou Planta", "amarelo"))
        print(colorir("3. Cuidar das Plantas (crescer)", "amarelo"))
        print(colorir("4. Alimentar Animais", "amarelo"))
        print(colorir("5. Colher Plantas", "amarelo"))
        print(colorir("6. Vender Produtos", "amarelo"))
        print(colorir("7. Vender Animais", "amarelo"))
        print(colorir("8. Vender Plantas", "amarelo"))
        print(colorir("9. Ver Status da Fazenda", "amarelo"))
        print(colorir(f"10. Encerrar o dia {fazenda.dia}", "amarelo"))
        if opcao_fabrica:
            print(colorir("11. Fábrica", "amarelo"))
        if opcao_lagoa:
            print(colorir("12. Lagoa dos Peixes", "amarelo"))
        
        ultima_opcao = 13 if opcao_lagoa else (12 if opcao_fabrica else 11)
        print(colorir(f"{ultima_opcao}. Sair do jogo", "vermelho"))

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print(colorir("❌ Digite apenas números válidos!", "vermelho"))
            continue

        if opcao == 1:
            comprar_item(fazenda)
        elif opcao == 2:
            escolher_animal_ou_planta(fazenda)
        elif opcao == 3:
            fazenda.crescendo()
        elif opcao == 4:
            fazenda.alimentar_animais()
        elif opcao == 5:
            fazenda.colher()
        elif opcao == 6:
            fazenda.vender_produtos()
        elif opcao == 7:
            fazenda.vender_animais()
        elif opcao == 8:
            fazenda.vender_plantas()
        elif opcao == 9:
            fazenda.exibir_status()
        elif opcao == 10:
            fazenda.encerra_dia()
        elif opcao_fabrica and opcao == 11:
            fabricar(fazenda)
        elif opcao_lagoa and opcao == 12:
            lagoa_dos_peixes(fazenda)
        elif opcao == ultima_opcao:
            print("Saindo do jogo... Até a próxima! 👋")
            break
        else:
            print(colorir("Opção inválida! Tente novamente.", "vermelho"))

def comprar_item(fazenda):
    mercadinho = {
        "Ração para Animais 🥣": {"preco": 8, "tipo": "animal"},
        "Pesticida 🧴": {"preco": 10, "tipo": "protecao"}
    }
    if fazenda.nivel >= 4:
        mercadinho["Arroz"] = {"preco": 10, "tipo": "ingrediente"}

    itens = list(mercadinho.keys())
    print("\n--- Mercadinho ---")
    for i, item in enumerate(itens):
        print(f"{i+1}. {item} - R$ {mercadinho[item]['preco']}")

    try:
        escolha = int(input("Escolha o item para comprar (número): ")) - 1
    except ValueError:
        print(colorir("❌ Digite apenas números válidos!", "vermelho"))
        return

    if escolha < 0 or escolha >= len(itens):
        print(colorir("❌ Opção inválida!", "vermelho"))
        return
    
    if not fazenda.gastar_energia(1): 
        return  


    item_nome = itens[escolha]
    item_info = mercadinho[item_nome]

    if fazenda.dinheiro >= item_info["preco"]:
        fazenda.dinheiro -= item_info["preco"]
        if item_info["tipo"] == "animal":
            fazenda.racao += 1
            print(f"Ração comprada! Agora você tem {fazenda.racao} unidades de ração.")
        elif item_info["tipo"] == "protecao":
            fazenda.protecao = True
            print("Pesticida comprado! Próximo ataque de praga será evitado.")
        elif item_info["tipo"] == "ingrediente":
            fazenda.estoque.append({"nome": item_nome, "preco": item_info["preco"]})
            fazenda.status_estoque.append(item_nome)
            print(f"Você comprou {item_nome} e ele foi adicionado ao estoque!")
    else:
        print(colorir("❌ Dinheiro insuficiente para comprar este item.", "vermelho"))

   



if __name__ == "__main__":
    main()

from package.animal import Vaca, Galinha, Ovelha, Porco
from package.planta import Milho, Trigo, Tomate, Rabanete
from utils import colorir 

def escolher_animal_ou_planta(fazenda):
    print("\n================ 🌾 Loja de Animais 🌾 ================")
    escolha_tipo = input("O que você deseja comprar?\n"
                     "1. 🌿 Planta\n"
                     "2. 🐄 Animal\n"
                     )
    print("==========================================================")

    limite_plantas, limite_animais = fazenda.limites()

    
    if escolha_tipo == "1":
        if len(fazenda.plantas) >= limite_plantas:
            print(colorir("🚫 Você atingiu o limite de plantas para o seu nível! Suba de nível para plantar mais.", "vermelho"))
            return
        plantas_disponiveis = [Milho(), Trigo()]  
        if fazenda.nivel >= 2:
            plantas_disponiveis.append(Tomate())
        if fazenda.nivel >= 4:
            plantas_disponiveis.append(Rabanete())

        print("\nPlantas disponíveis para compra:")
        for i, planta in enumerate(plantas_disponiveis, start=1):
            print(f"{i}. {planta.nome} - R$ {planta.custo}")

        escolha_planta = input("Escolha uma planta ou Enter para pular: ")
        if escolha_planta.isdigit() and 1 <= int(escolha_planta) <= len(plantas_disponiveis):
            fazenda.plantar(plantas_disponiveis[int(escolha_planta)-1])
        elif escolha_planta != "":
            print(colorir("🚫 Opção inválida.", "vermelho"))

    elif escolha_tipo == "2":
        if len(fazenda.animais) >= limite_animais:
            print(colorir("🚫 Você atingiu o limite de animais para o seu nível! Suba de nível para ter mais.", "vermelho"))
            return
        animais_disponiveis = [Vaca(), Galinha()]  
        if fazenda.nivel >= 3:
            animais_disponiveis.append(Ovelha())
        if fazenda.nivel >= 5:
            animais_disponiveis.append(Porco())

        print("\nAnimais disponíveis para compra:")
        for i, animal in enumerate(animais_disponiveis, start=1):
            print(f"{i}. {animal.nome} - R$ {animal.preco}")

        escolha_animal = input("Escolha um animal ou Enter para pular: ")
        if escolha_animal.isdigit() and 1 <= int(escolha_animal) <= len(animais_disponiveis):
            fazenda.adicionar_animal(animais_disponiveis[int(escolha_animal)-1])
        elif escolha_animal != "":
            print(colorir("❌Opção inválida.", "vermelho"))
    
    else: 
        print(colorir("❌ Opção inválida.", "vermelho"))

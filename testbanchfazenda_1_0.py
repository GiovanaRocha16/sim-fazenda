# tests/test_fazenda.py

from package.fazenda import Fazenda
from package.planta import Milho, Trigo, Tomate
from package.animal import Vaca, Galinha, Ovelha


def testar_fazenda():
    print("=== Teste da Classe Fazenda ===")

    # Criando uma fazenda
    fazenda = Fazenda("Fazenda da Gih")
    fazenda.dinheiro = 200  # dando um dinheiro inicial pra testar
    fazenda.exibir_status()

    # Comprando e plantando
    print("--- Plantando algumas culturas ---")
    fazenda.plantar(Milho())
    fazenda.plantar(Trigo())
    fazenda.plantar(Tomate())
    fazenda.exibir_status()

    # Crescendo e colhendo as plantas
    print("--- Fase de crescimento ---")
    fazenda.crescendo()

    print("--- Colhendo as plantações ---")
    fazenda.colher()
    fazenda.exibir_status()

    # Comprando animais
    print("--- Comprando alguns animais ---")
    fazenda.adicionar_animal(Vaca())
    fazenda.adicionar_animal(Galinha())
    fazenda.adicionar_animal(Ovelha())
    fazenda.exibir_status()

    # Alimentando os animais
    print("--- Alimentando os animais ---")
    fazenda.alimentar_animais()
    fazenda.exibir_status()

    # Vendendo produtos
    print("--- Vendendo produtos do estoque ---")
    fazenda.vender_produtos()
    fazenda.exibir_status()

    # Vendendo animais
    print("--- Vendendo animais ---")
    fazenda.vender_animais()
    fazenda.exibir_status()

    # Vendendo plantas restantes
    print("--- Vendendo plantas restantes ---")
    fazenda.vender_plantas()
    fazenda.exibir_status()


# Executa se rodar diretamente
if __name__ == "__main__":
    testar_fazenda()

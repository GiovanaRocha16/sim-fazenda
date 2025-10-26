# tests/test_animais.py

from package.animal import Animal, Vaca, Galinha, Ovelha

def workspace():
    print("=== Teste das classes de Animal ===")

    # Testando instâncias
    vaca = Vaca()
    galinha = Galinha()
    ovelha = Ovelha()

    print(f"Criado animal: {vaca.nome}, preço: {vaca.preco}, produto: {vaca.produto}")
    print(f"Criado animal: {galinha.nome}, preço: {galinha.preco}, produto: {galinha.produto}")
    print(f"Criado animal: {ovelha.nome}, preço: {ovelha.preco}, produto: {ovelha.produto}")

    # Testando o método alimentar()
    print("\n--- Alimentando os animais ---")
    vaca.alimentar()
    galinha.alimentar()
    ovelha.alimentar()

    # Testando o comportamento quando já foram alimentados
    print("\n--- Tentando alimentar de novo ---")
    vaca.alimentar()
    galinha.alimentar()
    ovelha.alimentar()

# Executa o teste se rodar direto o arquivo
if __name__ == "__main__":
    workspace()

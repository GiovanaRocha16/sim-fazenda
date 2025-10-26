# tests/test_plantas.py

from package.planta import Planta, Milho, Trigo, Tomate

def workspace():
    print("=== Teste das classes de Planta ===")

    # Testando instâncias
    milho = Milho()
    trigo = Trigo()
    tomate = Tomate()

    print(f"Criada planta: {milho.nome}, custo: {milho.custo}")
    print(f"Criada planta: {trigo.nome}, custo: {trigo.custo}")
    print(f"Criada planta: {tomate.nome}, custo: {tomate.custo}")

    # Testando o método crescer()
    print("\n--- Fase de crescimento ---")
    milho.crescer()
    trigo.crescer()
    tomate.crescer()

    # Testando o método colher()
    print("\n--- Colhendo as plantas ---")
    milho.colher()
    trigo.colher()
    tomate.colher()

    # Tentando colher novamente (erro esperado)
    print("\n--- Tentando colher novamente ---")
    milho.colher()
    trigo.colher()
    tomate.colher()

# Executa o teste se rodar direto o arquivo
if __name__ == "__main__":
    workspace()

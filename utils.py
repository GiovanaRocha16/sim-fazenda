def colorir(texto, cor):
    cores = {
        "verde": "\033[92m",
        "vermelho": "\033[91m",
        "amarelo": "\033[93m",
        "azul": "\033[94m",
        "roxo": "\033[95m",
        "reset": "\033[0m"
    }
    return f"{cores[cor]}{texto}{cores['reset']}"
class Planta:
    def __init__(self, nome, custo):
        self.nome = nome
        self.custo = custo
        self.crescida = False

    def crescer(self):
        if not self.crescida:
            self.crescida = True
            print(f"A planta {self.nome} cresceu e está pronta para ser colhida!")
            return True
        else:
            print(f"A planta {self.nome} já cresceu.")
            return False 

    def colher(self):
        if self.crescida:
            self.crescida = False
            print(f"A planta {self.nome} foi colhida!")
            return self.nome
        else:
            print(f"A planta {self.nome} ainda não está pronta para colheita.")
            return None

class Milho(Planta):
    def __init__(self):
        super().__init__("Milho", custo=10)


class Trigo(Planta):
    def __init__(self):
        super().__init__("Trigo", custo=8)


class Tomate(Planta):
    def __init__(self):
        super().__init__("Tomate", custo=15)

class Rabanete(Planta):
    def __init__(self):
        super().__init__("Rabanete", custo=18)

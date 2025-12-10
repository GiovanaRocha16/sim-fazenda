class Animal:
    def __init__(self, nome, preco, produto, dias_para_produzir ):
        self.nome = nome
        self.preco = preco
        self.produto = produto
        self.alimentado = False
        self.dias_para_produzir = dias_para_produzir
        self.dias_alimentado_consecutivo = 0

    def alimentar(self):
        
        if not self.alimentado:
            self.alimentado = True
            self.dias_alimentado_consecutivo += 1
            if self.dias_alimentado_consecutivo >= self.dias_para_produzir or self.dias_para_produzir == 1:
                print(f"{self.nome} foi alimentado e produziu {self.produto}!")
                self.dias_alimentado_consecutivo = 0
                return self.produto
            else:
                print(f"{self.nome} foi alimentada hoje ({self.dias_alimentado_consecutivo}/{self.dias_para_produzir})")
                return None
        else:
            print(f"{self.nome} já foi alimentada hoje.")
            return None 
        
    def passar_dia(self):
        if not self.alimentado:
            self.dias_alimentado_consecutivo = 0
        self.alimentado = False  

class Vaca(Animal):
    def __init__(self):
        super().__init__("Vaca", 60, "Leite", 3)


class Galinha(Animal):
    def __init__(self):
        super().__init__("Galinha", 20, "Ovos", 1)

class Ovelha(Animal):
    def __init__(self):
        super().__init__("Ovelha", 35, "Lã", 2)

class Porco(Animal):
    def __init__(self):
        super().__init__("Porco", 50, "Bacon", 4)
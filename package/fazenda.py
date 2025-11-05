import random
class Fazenda:
    def __init__(self, nome):
        self.nome = nome
        self.plantas = []       
        self.animais = []       
        self.estoque = []       
        self.status_estoque = []
        self.dinheiro = 50       
        self.dia = 1
        self.protecao = False
        self.racao = 0
        self.nivel = 1
        self.energia_maxima = self.calcular_energia_maxima()
        self.energia = self.energia_maxima
        self.xp = 0
        self.xp_para_proximo_nivel = 50
        self.plantas_desbloqueadas = ["Milho", "Trigo"]  
        self.animais_desbloqueados = ["Galinha", "Vaca"] 
    

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        print(f"Você ganhou {quantidade} XP! Total: {self.xp}/{self.xp_para_proximo_nivel}")

        while self.xp >= self.xp_para_proximo_nivel:
            self.subir_nivel()
    
    def calcular_energia_maxima(self):
        return 10 + (self.nivel - 1) * 2

    def subir_nivel(self):
        self.nivel += 1
        self.xp -= self.xp_para_proximo_nivel
        self.xp_para_proximo_nivel = int(self.xp_para_proximo_nivel * 1.5)
        self.energia_maxima = self.calcular_energia_maxima()
        print(f"🎉 Parabéns! Sua fazenda subiu para o nível {self.nivel}!")
        print(f"⚡ Energia máxima aumentou para {self.energia_maxima}!")

    # Desbloqueio
        if self.nivel == 2:
            self.plantas_desbloqueadas.append("Tomate")
            print("🍅 Tomate desbloqueado!")
        if self.nivel == 3:
            self.animais_desbloqueados.append("Ovelha")
            print("🐑 Ovelha desbloqueada!")    
        if self.nivel == 3:
            print("🏭 Fábrica desbloqueada!")   
        if self.nivel == 4:
            self.plantas_desbloqueadas.append("Rabanete")
            print("🌱 Rabanete desbloqueado!")
        if self.nivel == 4:
            print("🐟 Lagoa dos peixes desbloqueada")
        if self.nivel == 5:
            self.animais_desbloqueados.append("Porco")
            print("🐖 Porco desbloqueado!")


    def gastar_energia(self, quantidade):
        if self.energia >= quantidade:
            self.energia -= quantidade
            return True
        else:
            print("⚠️ Você está sem energia suficiente para realizar essa ação!")
            return False
        
    def encerra_dia(self):
        print(f"\n--- Resumo do Dia {self.dia} ---")
        print(f"Plantas na fazenda: {[p.nome for p in self.plantas]}")
        print(f"Animais na fazenda: {[a.nome for a in self.animais]}")
        print(f"Estoque: {self.status_estoque}")
        print(f"Dinheiro: R$ {self.dinheiro:.2f}")
        print("---------------------------\n")

        if self.protecao:
            print("Pesticida protegeu suas plantas hoje!")
            self.protecao = False
        else:
            if self.plantas:
                chance_praga = 0.2
                if random.random() < chance_praga:
                    qtd_perdida = random.randint(1, len(self.plantas))
                    perdidas = random.sample(self.plantas, qtd_perdida)
                    for planta in perdidas:
                        self.plantas.remove(planta)
                    nomes_perdidos = [p.nome for p in perdidas]
                    print(f"Pragas atacaram a fazenda! As plantas {nomes_perdidos} foram destruídas!")
        
       
        for animal in self.animais:
            animal.passar_dia()

        self.energia = self.energia_maxima
        print(f"💤 Você descansou e recuperou sua energia total ({self.energia_maxima}).")

        self.dia += 1



    def get_dinheiro(self):
        return self.dinheiro

    def plantar(self, planta):
          
        if self.dinheiro >= planta.custo:
            self.plantas.append(planta)
            self.dinheiro -= planta.custo
            if self.gastar_energia(1):
                print(f"Você plantou {planta.nome}, e agora está com {self.energia} de energia!")
                self.ganhar_xp(5)
        else:
            print("Dinheiro insuficiente para plantar.")

    def crescendo(self):

        if not self.plantas:
            print("🌱 Não há plantas para crescer.")
            return
        
        if not self.gastar_energia(1):
            print("⚠️ Você está sem energia suficiente para realizar essa ação!")
            return
        
        for planta in self.plantas:
            cresceu = planta.crescer()
            if cresceu:
                self.ganhar_xp(2)

    def colher(self):
        
        if not self.plantas:
            print("⚠️ Não há plantas cadastradas na fazenda.")
            return
        
        if not self.gastar_energia(1):
            print("⚠️ Você está sem energia suficiente para realizar essa ação!")
            return
        
        precos = {"Milho": 4, "Trigo": 2, "Tomate": 8, "Rabanete": 11}
        
        for planta in self.plantas:
                produto = planta.colher()
                if produto:
                    self.estoque.append({"nome": produto, "preco": precos[produto]})
                    self.status_estoque.append(produto)
                    self.ganhar_xp(2)

    def adicionar_animal(self, animal):
        if self.dinheiro < animal.preco:
            print("Dinheiro insuficiente para comprar o animal.")
            return
        if not self.gastar_energia(1):
            print("⚠️ Você está sem energia suficiente para realizar essa ação!")
            return
        self.animais.append(animal)
        self.dinheiro -= animal.preco
        print(f"Você comprou um(a) {animal.nome}!")
        self.ganhar_xp(5)

    def alimentar_animais(self):
        if not self.animais:
            print("Não há animais na fazenda.")
            return

        if self.racao <= 0:
            print("Você não tem ração para alimentar os animais!")
            return
        
        if not self.gastar_energia(1):  
            return
        
        precos_produto = {"Leite": 10, "Ovos": 5, "Lã": 8, "Bacon": 15}

        for animal in self.animais:
            produto = animal.alimentar()

            if produto:
                self.estoque.append({"nome": produto, "preco": precos_produto[produto]})
                self.status_estoque.append(produto)
                self.ganhar_xp(4)
                
        
        self.racao -= 1  
        print(f"Ração restante: {self.racao}")



    def vender_produtos(self):
        
        if not self.estoque:
            print("Não há produtos para vender.")
            return
        if not self.gastar_energia(1):  
            return

        total = sum(item["preco"] for item in self.estoque)
        self.dinheiro += total

        print(f"Você vendeu {len(self.estoque)} produto(s) e ganhou R$ {total:.2f}!")
        self.ganhar_xp(6)
        self.estoque.clear()
        self.status_estoque.clear()


    def vender_animais(self):
        
        if not self.animais:
            print("Você não tem animais para vender.")
            return
        
        if not self.gastar_energia(1):  
            return

        ganhos = len(self.animais) * 20 
        self.dinheiro += ganhos
        print(f"Você vendeu {len(self.animais)} animais e ganhou {ganhos} moedas!")
        self.ganhar_xp(3)
        self.animais.clear()


    def vender_plantas(self):
        
        if not self.plantas:
            print("Você não tem plantas para vender.")
            return
        
        if not self.gastar_energia(1):  
            return

        ganhos = len(self.plantas) * 10  
        self.dinheiro += ganhos
        print(f"Você vendeu {len(self.plantas)} plantas e ganhou {ganhos} moedas!")
        self.ganhar_xp(3)
        self.plantas.clear()

 
    def exibir_status(self):
        print("\n--- STATUS DA FAZENDA ---")
        print(f"Nome: {self.nome}")
        print(f"Dinheiro: R$ {self.dinheiro:.2f}")
        print(f"Plantações: {[p.nome for p in self.plantas]}")
        print(f"Animais: {[a.nome for a in self.animais]}")
        print(f"Estoque: {self.status_estoque}")
        print(f"Dia: {self.dia}")
        print(f"Energia: {self.energia}")
        print(f"Nível: {self.nivel}")
        print("---------------------------\n")

    def limites(self):
        if self.nivel == 1:
            return 3, 3  
        elif self.nivel == 2:
            return 5, 4
        elif self.nivel == 3:
            return 6, 4
        elif self.nivel == 4:
            return 7, 5
        elif self.nivel == 5:
            return 8, 6
        elif self.nivel == 6:
            return 10, 7
        elif self.nivel == 7:
            return 12, 8
        elif self.nivel == 8:
            return 13, 9
        else:
            return 15, 10

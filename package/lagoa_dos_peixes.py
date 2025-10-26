import random

def lagoa_dos_peixes(fazenda):
    if not fazenda.gastar_energia(3):
        print("⚠️ Você está sem energia suficiente para pescar!")
        return

    print("\n🎣 Você foi até a Lagoa dos Peixes...")
    print("⏳ Jogando a vara de pescar...")

    # Pequena chance de o peixe escapar
    if random.random() < 0.2:
        print("💨 O peixe escapou! Que pena...")
        return

    # Escolher tipo de peixe
    tipo_peixe = random.choices(
        ["comum", "raro"],
        weights=[0.8, 0.2],  
        k=1
    )[0]

    precos = {"Peixe Comum": 10, "Peixe Raro": 30}

    if tipo_peixe == "comum":
        print("\033[33m🐟 Você pescou um Peixe Comum!\033[0m") 
        fazenda.estoque.append({"nome": "Peixe Comum", "preco": precos["Peixe Comum"]})
        fazenda.status_estoque.append("Peixe Comum")
        fazenda.ganhar_xp(4)
    else:
        print("\033[35m🐠 Uau! Você pescou um Peixe RARO!\033[0m")  
        fazenda.estoque.append({"nome": "Peixe Raro", "preco": precos["Peixe Raro"]})
        fazenda.status_estoque.append("Peixe Raro")
        fazenda.ganhar_xp(8)

    print("✨ O peixe foi adicionado ao estoque!")

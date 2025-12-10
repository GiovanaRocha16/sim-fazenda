import tkinter as tk
from package.animal import Vaca, Galinha, Ovelha, Porco
from package.planta import Milho, Trigo, Tomate, Rabanete

def escolher_animal_ou_planta_gui(fazenda, frame_conteudo):
    # Função para limpar área de conteúdo
    def limpar():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    limpar()

    # ---------- Estilos ----------
    bg_principal = "#f3f8e6"   # fundo suave
    cor_titulo = "#6fb96f"     # verde da fazenda
    cor_botao_animal = "#f7d794"
    cor_botao_planta = "#a4de9f"
    cor_botao_voltar = "#ff6b6b"

    frame_conteudo.config(bg=bg_principal)

    # ---------- Cabeçalho ----------
    header = tk.Frame(frame_conteudo, bg=cor_titulo, height=60)
    header.pack(fill="x")
    tk.Label(
        header,
        text="🌾 Loja da Fazenda",
        font=("Arial", 18, "bold"),
        bg=cor_titulo,
        fg="white"
    ).pack(pady=10)

    # ---------- Texto principal ----------
    tk.Label(
        frame_conteudo,
        text="O que você deseja comprar?",
        font=("Arial", 14),
        bg=bg_principal
    ).pack(pady=15)

    # ---------- Subtelas ----------
    def abrir_loja_animais():
        limpar()
        header = tk.Frame(frame_conteudo, bg="#d0a86e", height=60)
        header.pack(fill="x")
        tk.Label(header, text="🐮 Loja de Animais", font=("Arial", 18, "bold"), bg="#d0a86e", fg="white").pack(pady=10)

        animais_disponiveis = [("Vaca", 60, Vaca), ("Galinha", 20, Galinha)]
        if fazenda.nivel >= 3:
            animais_disponiveis.append(("Ovelha", 35, Ovelha))
        if fazenda.nivel >= 5:
            animais_disponiveis.append(("Porco", 50, Porco))

        frame_lista = tk.Frame(frame_conteudo, bg=bg_principal)
        frame_lista.pack(pady=10)

        for nome, preco, classe in animais_disponiveis:
            tk.Button(
                frame_lista,
                text=f"{nome} - R${preco}",
                font=("Arial", 12),
                width=25,
                bg=cor_botao_animal,
                relief="raised",
                command=lambda c=classe: [
                    fazenda.adicionar_animal(c()),
                    escolher_animal_ou_planta_gui(fazenda, frame_conteudo)
                ]
            ).pack(pady=5)

        tk.Button(
            frame_conteudo,
            text="⬅ Voltar à Loja",
            font=("Arial", 12),
            bg=cor_botao_voltar,
            fg="white",
            width=20,
            command=lambda: escolher_animal_ou_planta_gui(fazenda, frame_conteudo)
        ).pack(pady=15)

    def abrir_loja_plantas():
        limpar()
        header = tk.Frame(frame_conteudo, bg="#7bc47f", height=60)
        header.pack(fill="x")
        tk.Label(header, text="🌿 Loja de Plantas", font=("Arial", 18, "bold"), bg="#7bc47f", fg="white").pack(pady=10)

        plantas_disponiveis = [("Milho", 10, Milho), ("Trigo", 8, Trigo)]
        if fazenda.nivel >= 2:
            plantas_disponiveis.append(("Tomate", 15, Tomate))
        if fazenda.nivel >= 4:
            plantas_disponiveis.append(("Rabanete", 18, Rabanete))

        frame_lista = tk.Frame(frame_conteudo, bg=bg_principal)
        frame_lista.pack(pady=10)

        for nome, preco, classe in plantas_disponiveis:
            tk.Button(
                frame_lista,
                text=f"{nome} - R${preco}",
                font=("Arial", 12),
                width=25,
                bg=cor_botao_planta,
                relief="raised",
                command=lambda c=classe: [
                    fazenda.plantar(c()),
                    escolher_animal_ou_planta_gui(fazenda, frame_conteudo)
                ]
            ).pack(pady=5)

        tk.Button(
            frame_conteudo,
            text="⬅ Voltar à Loja",
            font=("Arial", 12),
            bg=cor_botao_voltar,
            fg="white",
            width=20,
            command=lambda: escolher_animal_ou_planta_gui(fazenda, frame_conteudo)
        ).pack(pady=15)

    # ---------- Botões principais ----------
    frame_botoes = tk.Frame(frame_conteudo, bg=bg_principal)
    frame_botoes.pack(pady=30)

    tk.Button(
        frame_botoes,
        text="🐮 Comprar Animal",
        font=("Arial", 13),
        bg=cor_botao_animal,
        width=20,
        command=abrir_loja_animais
    ).pack(pady=8)

    tk.Button(
        frame_botoes,
        text="🌿 Comprar Planta",
        font=("Arial", 13),
        bg=cor_botao_planta,
        width=20,
        command=abrir_loja_plantas
    ).pack(pady=8)

    tk.Button(
        frame_conteudo,
        text="❌ Fechar Loja",
        font=("Arial", 12),
        bg=cor_botao_voltar,
        fg="white",
        width=20,
        command=limpar
    ).pack(pady=25)

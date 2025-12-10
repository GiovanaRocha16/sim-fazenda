import tkinter as tk
from PIL import Image, ImageTk
import os
from banco import criar_tabelas, carregar_fazenda, salvar_fazenda
from package.fazenda import Fazenda
from interface_jogo import abrir_interface_jogo

def iniciar_jogo(event=None):
    root.destroy()
    criar_tabelas()
    fazenda = carregar_fazenda()
    if fazenda is None:
        # Aqui você pode abrir uma janela para o usuário digitar o nome da fazenda
        fazenda = Fazenda("Minha Fazenda")
        salvar_fazenda(fazenda)
    abrir_interface_jogo(fazenda)

    print("Jogo iniciado!")

# --- Tela Inicial ---
root = tk.Tk()
root.title("Sim Fazenda - Início")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())  # ESC para sair

# Canvas
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Fundo ---
fundo_path = os.path.join(os.path.dirname(__file__), "tela_inicial.png")
fundo_original = Image.open(fundo_path).convert("RGBA")

# --- Botão ---
botao_path = os.path.join(os.path.dirname(__file__), "botao_jogar.png")
botao_original = Image.open(botao_path).convert("RGBA")

# Variáveis globais
btn = None
fundo_item = None
botao_tk_ref = []
new_w = None
new_h = None
fundo_tk = None

# --- Função para atualizar fundo e botão ---
def atualizar_tela(event=None):
    global fundo_tk, botao_tk_ref, btn, fundo_item, new_w, new_h

    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    if screen_width < 10 or screen_height < 10:
        return

    # Redimensiona o fundo
    fundo = fundo_original.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    fundo_tk = ImageTk.PhotoImage(fundo)

    if fundo_item is None:
        fundo_item = canvas.create_image(0, 0, anchor="nw", image=fundo_tk)
    else:
        canvas.itemconfig(fundo_item, image=fundo_tk)

    # Redimensiona o botão proporcional à largura da tela (15%)
    largura_desejada = int(screen_width * 0.40)
    w_original, h_original = botao_original.size
    scale = largura_desejada / w_original
    new_w = max(int(w_original * scale), 1)
    new_h = max(int(h_original * scale), 1)
    botao = botao_original.resize((new_w, new_h), Image.Resampling.LANCZOS)
    botao_tk = ImageTk.PhotoImage(botao)

    # Mantém referência da imagem para não sumir
    botao_tk_ref.clear()
    botao_tk_ref.append(botao_tk)

    # Posiciona o botão
    btn_x = screen_width // 2
    btn_y = int(screen_height * 0.85)

    # Cria o botão apenas uma vez
    if btn is None:
        btn_id = canvas.create_image(btn_x, btn_y, image=botao_tk)
        globals()['btn'] = btn_id
    else:
        canvas.coords(btn, btn_x, btn_y)
        canvas.itemconfig(btn, image=botao_tk)

# Inicializa tela
atualizar_tela()

# Atualiza quando a janela for redimensionada
root.bind("<Configure>", atualizar_tela)

# --- Clique apenas em pixels visíveis do botão ---
def click_botao(event):
    global btn
    coords = canvas.coords(btn)
    x_rel = int(event.x - (coords[0] - new_w / 2))
    y_rel = int(event.y - (coords[1] - new_h / 2))

    if 0 <= x_rel < new_w and 0 <= y_rel < new_h:
        pixel = botao_original.resize((new_w, new_h), Image.Resampling.LANCZOS).getpixel((x_rel, y_rel))
        if pixel[3] != 0:
            iniciar_jogo()

canvas.bind("<Button-1>", click_botao)

root.mainloop()

import tkinter as tk
from tkinter import simpledialog, messagebox 
import random
import os

pending_message = None

try:
    from banco import criar_tabelas, carregar_fazenda, salvar_fazenda
except Exception as e:
    print("Aviso: não foi possível importar banco.py.", e)  
    import pickle
    def criar_tabelas(): return
    def salvar_fazenda(fazenda):
        with open('save_fazenda_gui.pkl', 'wb') as f:
            pickle.dump(fazenda, f)
    def carregar_fazenda():
        if os.path.exists('save_fazenda_gui.pkl'):
            with open('save_fazenda_gui.pkl','rb') as f:
                return pickle.load(f)
        return None

try:
    from package.fazenda import Fazenda
    from package.animal import Vaca, Galinha, Ovelha, Porco
    from package.planta import Milho, Trigo, Tomate, Rabanete
except Exception as _:
    class Animal:
        def __init__(self, nome, preco, produto, dias_para_produzir):
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
                if self.dias_alimentado_consecutivo >= self.dias_para_produzir:
                    self.dias_alimentado_consecutivo = 0
                    return self.produto
            return None
        def passar_dia(self):
            if not self.alimentado:
                self.dias_alimentado_consecutivo = 0
            self.alimentado = False
    class Vaca(Animal):
        def __init__(self):
            super().__init__('Vaca',60,'Leite',3)
    class Galinha(Animal):
        def __init__(self):
            super().__init__('Galinha',20,'Ovos',1)
    class Ovelha(Animal):
        def __init__(self):
            super().__init__('Ovelha',35,'Lã',2)
    class Porco(Animal):
        def __init__(self):
            super().__init__('Porco',50,'Bacon',4)
    class Planta:
        def __init__(self, nome, custo):
            self.nome = nome
            self.custo = custo
            self.crescida = False
        def crescer(self):
            if not self.crescida:
                self.crescida = True
                return True
            return False
        def colher(self):
            if self.crescida:
                self.crescida = False
                return self.nome
            return None
    class Milho(Planta):
        def __init__(self):
            super().__init__('Milho',10)
    class Trigo(Planta):
        def __init__(self):
            super().__init__('Trigo',8)
    class Tomate(Planta):
        def __init__(self):
            super().__init__('Tomate',15)
    class Rabanete(Planta):
        def __init__(self):
            super().__init__('Rabanete',18)
    class Fazenda:
        def __init__(self,nome):
            self.nome = nome
            self.fazenda = None
            self.pending_message = None  
            self.plantas = []
            self.animais = []
            self.estoque = []
            self.status_estoque = []
            self.dinheiro = 50
            self.dia = 1
            self.protecao = False
            self.racao = 0
            self.nivel = 1
            self.energia_maxima = 10
            self.energia = 10
            self.xp = 0
            self.xp_para_proximo_nivel = 50
            self.plantas_desbloqueadas = ['Milho','Trigo']
            self.animais_desbloqueados = ['Galinha','Vaca']
        def ganhar_xp(self,q): self.xp += q
        def calcular_energia_maxima(self): return 10 + (self.nivel-1)*2
        def gastar_energia(self,q):
            if self.energia >= q:
                self.energia -= q
                return True
            return False
        def crescer(self):
            for p in self.plantas: p.crescer()
        def colher(self):
            for p in list(self.plantas):
                prod = p.colher()
                if prod:
                    preco = {'Milho':4,'Trigo':2,'Tomate':8,'Rabanete':11}.get(prod,5)
                    self.estoque.append({'nome':prod,'preco':preco})
                    self.status_estoque.append(prod)
        def alimentar_animais(self):
            for a in self.animais:
                prod = a.alimentar()
                if prod:
                    self.estoque.append({'nome':prod,'preco':10})
                    self.status_estoque.append(prod)
        def vender_produtos(self):
            total = sum(i['preco'] for i in self.estoque)
            self.dinheiro += total
            self.estoque.clear(); self.status_estoque.clear()
            return total
        def vender_animais(self):
            ganhos = len(self.animais)*20
            self.dinheiro += ganhos; self.animais.clear()
            return ganhos
        def vender_plantas(self):
            ganhos = len(self.plantas)*10
            self.dinheiro += ganhos; self.plantas.clear()
            return ganhos
        def adicionar_animal(self,a):
            if self.dinheiro >= a.preco:
                self.animais.append(a); self.dinheiro -= a.preco
        def plantar(self,p):
            if self.dinheiro >= p.custo:
                self.plantas.append(p); self.dinheiro -= p.custo
        def encerra_dia(self):
            for a in self.animais: a.passar_dia()
            self.energia = self.calcular_energia_maxima(); self.dia += 1
        def limites(self):
            if self.nivel == 1: return 3,3
            elif self.nivel == 2: return 5,4
            elif self.nivel == 3: return 6,4
            elif self.nivel == 4: return 7,5
            elif self.nivel == 5: return 8,6
            elif self.nivel == 6: return 10,7
            elif self.nivel == 7: return 12,8
            elif self.nivel == 8: return 13,9
            else: return 15,10

THEME_BG = '#dff7ff'   
SIDE = '#fffaf0'
ACCENT = '#ffd27f'
BTN = '#7bdff6'
BTN2 = '#b7ffb3'
TEXT = '#1e1e1e'
LOCKED = '#e7e7e7'

ICONS = {
    'Milho':'🌽','Trigo':'🌾','Tomate':'🍅','Rabanete':'🥕',
    'Galinha':'🐔','Vaca':'🐄','Ovelha':'🐑','Porco':'🐖',
    'Leite':'🥛','Ovos':'🥚','Lã':'🧶','Bacon':'🥓','Peixe Comum':'🐟','Peixe Raro':'🐠'
}
def emoji(nome): return ICONS.get(nome,'')

# ---------- FUNÇÃO PRINCIPAL ----------

def abrir_interface_jogo(fazenda=None):
    criar_tabelas()  

    if fazenda is None:
        fazenda = carregar_fazenda()

    root = tk.Tk()
    root.title("Sim Fazenda - Alegre")
    root.configure(bg=THEME_BG)
    root.geometry("1100x650")
    root.minsize(900,600)

    welcome_frame = tk.Frame(root, bg=THEME_BG)
    main_frame = tk.Frame(root, bg=SIDE)  

    def set_pending_message(text):
        global pending_message
        pending_message = text

    def show_welcome():
        welcome_frame.pack(fill='both', expand=True)
        main_frame.forget()

        welcome_frame.configure(bg=THEME_BG)
        for w in welcome_frame.winfo_children(): w.destroy()
        title = tk.Label(welcome_frame, text="🌻 Bem-vindo ao Sim Fazenda! 🌻", font=(None,22,'bold'), bg=THEME_BG, fg=TEXT)
        title.pack(pady=(40,10))
        subtitle = tk.Label(welcome_frame, text="Crie o nome da sua fazenda e comece a jogar", bg=THEME_BG, fg=TEXT)
        subtitle.pack(pady=(0,20))

        card = tk.Frame(welcome_frame, bg=SIDE, padx=20, pady=20)
        card.pack(pady=10)
        lbl = tk.Label(card, text="Nome da Fazenda", bg=SIDE, font=(None,12))
        lbl.pack(anchor='w')
        entry_name = tk.Entry(card, font=(None,14), width=28)
        entry_name.pack(pady=8)
        hint = tk.Label(card, text="Ex: Fazenda do Sol, Sítio da Gih, etc.", bg=SIDE, fg='#666666')
        hint.pack(anchor='w')

        def começar():
            nome = entry_name.get().strip()
            if not nome:
                lbl_msg_welcome.config(text="⚠️ Digite um nome antes de começar.", fg='red')
                return
            nonlocal fazenda
            fazenda = Fazenda(nome)
            salvar_fazenda(fazenda)
            set_pending_message(f"Bem-vinda(o), {fazenda.nome}! Desenvolva sua fazendinha!")
            show_main()

        btn_start = tk.Button(card, text="Começar 🌱", bg=ACCENT, font=(None,14,'bold'), width=20, command=começar)
        btn_start.pack(pady=(12,4))

        lbl_msg_welcome = tk.Label(card, text="", bg=SIDE)
        lbl_msg_welcome.pack()

        if fazenda is not None:
            entry_name.insert(0, fazenda.nome)
            btn_use_saved = tk.Button(card, text="Usar save atual", bg=BTN2, command=começar)
            btn_use_saved.pack(pady=(6,0))

    def show_main():
        welcome_frame.forget()
        main_frame.pack(fill='both', expand=True)
        build_main_ui()

    def build_main_ui():
        global pending_message
        for w in main_frame.winfo_children(): w.destroy()

        left = tk.Frame(main_frame, bg=SIDE, width=300, padx=12, pady=12)
        left.pack(side='left', fill='y')
        center = tk.Frame(main_frame, bg=THEME_BG, padx=12, pady=12)
        center.pack(side='left', fill='both', expand=True)
        right = tk.Frame(main_frame, bg=SIDE, width=300, padx=12, pady=12)
        right.pack(side='right', fill='y')

        lbl_name = tk.Label(left, text=f"🌻 {fazenda.nome}", font=(None,18,'bold'), bg=SIDE, fg=TEXT)
        lbl_name.pack(anchor='w')

        var_money = tk.StringVar(value=f"R$ {fazenda.dinheiro:.2f}")
        lbl_money = tk.Label(left, textvariable=var_money, bg=SIDE, fg=TEXT, font=(None,12))
        lbl_money.pack(anchor='w', pady=6)

        var_day = tk.StringVar(value=f"Dia: {fazenda.dia}")
        lbl_day = tk.Label(left, textvariable=var_day, bg=SIDE, fg=TEXT)
        lbl_day.pack(anchor='w')

        var_energy = tk.StringVar(value=f"Energia: {fazenda.energia}/{fazenda.energia_maxima}")
        lbl_energy = tk.Label(left, textvariable=var_energy, bg=SIDE, fg=TEXT)
        lbl_energy.pack(anchor='w', pady=4)

        var_level = tk.StringVar(value=f"Nível: {fazenda.nivel}  XP: {fazenda.xp}/{fazenda.xp_para_proximo_nivel}")
        lbl_level = tk.Label(left, textvariable=var_level, bg=SIDE, fg=TEXT, wraplength=260)
        lbl_level.pack(anchor='w', pady=4)

        btn_save = tk.Button(left, text='💾 Salvar', bg=BTN, command=lambda: (salvar_fazenda(fazenda), set_message("💾 Jogo salvo.")))
        btn_save.pack(fill='x', pady=6)
        btn_save_exit = tk.Button(left, text='💾 Salvar e Sair', bg=BTN, command=lambda: (salvar_fazenda(fazenda), root.destroy()))
        btn_save_exit.pack(fill='x', pady=6)

        nonlocal_lbl = {}
        initial_msg = pending_message if pending_message else "Bem-vinda(o)! Use somente botões (exceto o nome no começo)."
        msg_var = tk.StringVar(value=initial_msg)
        nonlocal_lbl['msg'] = msg_var
        lbl_msg = tk.Label(left, textvariable=msg_var, bg=SIDE, fg=TEXT, wraplength=260, justify='left')
        lbl_msg.pack(anchor='w', pady=12)
        pending_message = None

        top = tk.Frame(center, bg=THEME_BG)
        top.pack(fill='x')

        plants_frame = tk.LabelFrame(top, text='🌱 Plantações', bg=THEME_BG, padx=6, pady=6)
        plants_frame.pack(side='left', fill='both', expand=True, padx=6, pady=6)
        animals_frame = tk.LabelFrame(top, text='🐾 Animais', bg=THEME_BG, padx=6, pady=6)
        animals_frame.pack(side='left', fill='both', expand=True, padx=6, pady=6)

        lb_plants = tk.Listbox(plants_frame, height=8)
        lb_plants.pack(fill='both', expand=True)
        lb_animals = tk.Listbox(animals_frame, height=8)
        lb_animals.pack(fill='both', expand=True)

        actions = tk.LabelFrame(center, text='🎮 Ações', bg=THEME_BG, padx=6, pady=6)
        actions.pack(fill='both', expand=True, padx=6, pady=6)

        estoque_frame = tk.LabelFrame(right, text='📦 Estoque', bg=SIDE, padx=6, pady=6)
        estoque_frame.pack(fill='both', expand=True)
        lb_stock = tk.Listbox(estoque_frame, width=36)
        lb_stock.pack(fill='both', expand=True)

        btn_sell_sel = tk.Button(estoque_frame, text='💵 Vender Selecionado', bg=BTN, command=lambda: vender_selecionado(lb_stock, msg_var))
        btn_sell_sel.pack(fill='x', pady=4)
        btn_sell_all = tk.Button(estoque_frame, text='💰 Vender Tudo', bg=BTN, command=lambda: vender_tudo(msg_var))
        btn_sell_all.pack(fill='x', pady=4)

        def set_message(text):
            msg_var.set(text)

        def atualizar_ui_all():
            lbl_name.config(text=f"🌻 {fazenda.nome}")
            var_money.set(f"R$ {fazenda.dinheiro:.2f}")
            var_day.set(f"Dia: {fazenda.dia}")
            var_energy.set(f"Energia: {fazenda.energia}/{fazenda.energia_maxima}")
            var_level.set(f"Nível: {fazenda.nivel}  XP: {fazenda.xp}/{fazenda.xp_para_proximo_nivel}")

            lb_plants.delete(0, 'end')
            for p in fazenda.plantas:
                estado = " (Pronta)" if getattr(p, 'crescida', False) else ""
                lb_plants.insert('end', f"{emoji(p.nome)} {p.nome}{estado}")

            lb_animals.delete(0, 'end')
            for a in fazenda.animais:
                aliment = " (Alimentado)" if getattr(a, 'alimentado', False) else ""
                lb_animals.insert('end', f"{emoji(a.nome)} {a.nome}{aliment}")

            lb_stock.delete(0, 'end')
            produtos = fazenda.get_produtos_disponiveis() if hasattr(fazenda, 'get_produtos_disponiveis') else None
            if produtos:
                for nome, qtd, preco in produtos:
                    lb_stock.insert('end', f"{emoji(nome)} {nome} x{qtd} - R$ {preco}")
            else:
                for it in fazenda.estoque:
                    lb_stock.insert('end', f"{emoji(it.get('nome'))} {it.get('nome')} - R$ {it.get('preco')}")

        def abrir_loja_panel():
            panel = tk.Toplevel(root)
            panel.title("Loja — Comprar")
            panel.configure(bg=THEME_BG)
            panel.geometry("520x520")

            header = tk.Label(panel, text="🛒 Loja — Comprar", font=(None,14,'bold'), bg=THEME_BG)
            header.pack(pady=8)

            limite_plantas, limite_animais = fazenda.limites() if hasattr(fazenda, 'limites') else (999,999)

            frame_p = tk.LabelFrame(panel, text="🌱 Plantas", bg=THEME_BG, padx=6, pady=6)
            frame_p.pack(fill='both', expand=True, padx=8, pady=6)
            plantas_disponiveis = [Milho, Trigo]
            if fazenda.nivel >= 2: plantas_disponiveis.append(Tomate)
            if fazenda.nivel >= 4: plantas_disponiveis.append(Rabanete)

            for cls in plantas_disponiveis:
                temp = cls()
                preco = getattr(temp, 'custo', 0)
                nome = temp.nome
                desbloqueado = len(fazenda.plantas) < limite_plantas
                text = f"{emoji(nome)} {nome} — R$ {preco}"
                btn_bg = BTN2 if desbloqueado else LOCKED
                btn = tk.Button(frame_p, text=text, bg=btn_bg, width=36,
                                command=lambda c=cls: comprar_planta(c, panel))
                if not desbloqueado:
                    btn.config(state='disabled')
                btn.pack(pady=4)

            frame_a = tk.LabelFrame(panel, text="🐮 Animais", bg=THEME_BG, padx=6, pady=6)
            frame_a.pack(fill='both', expand=True, padx=8, pady=6)
            animais_disponiveis = [Galinha, Vaca]
            if fazenda.nivel >= 3: animais_disponiveis.append(Ovelha)
            if fazenda.nivel >= 5: animais_disponiveis.append(Porco)

            for cls in animais_disponiveis:
                temp = cls()
                preco = getattr(temp, 'preco', 0)
                nome = temp.nome
                desbloqueado = len(fazenda.animais) < limite_animais
                text = f"{emoji(nome)} {nome} — R$ {preco}"
                btn_bg = BTN if desbloqueado else LOCKED
                btn = tk.Button(frame_a, text=text, bg=btn_bg, width=36,
                                command=lambda c=cls: comprar_animal(c, panel))
                if not desbloqueado:
                    btn.config(state='disabled')
                btn.pack(pady=4)

        def comprar_planta(cls, parent_panel=None):
            p = cls()
            preco = getattr(p, 'custo', 0)
            limite_plantas, _ = fazenda.limites() if hasattr(fazenda, 'limites') else (999,999)
            if len(fazenda.plantas) >= limite_plantas:
                set_message("🚫 Limite de plantas atingido para seu nível.")
                return
            if not fazenda.gastar_energia(1):
                set_message("⚠️ Energia insuficiente para plantar.")
                return
            if fazenda.dinheiro < preco:
                set_message(f"💸 Dinheiro insuficiente. {p.nome} custa R$ {preco}.")
                return
            fazenda.plantar(p)
            set_message(f"🌱 Plantou {p.nome} por R$ {preco}.")
            atualizar_ui_all()
            if parent_panel: parent_panel.destroy()

        def comprar_animal(cls, parent_panel=None):
            a = cls()
            preco = getattr(a, 'preco', 0)
            _, limite_animais = fazenda.limites() if hasattr(fazenda, 'limites') else (999,999)
            if len(fazenda.animais) >= limite_animais:
                set_message("🚫 Limite de animais atingido para seu nível.")
                return
            if not fazenda.gastar_energia(1):
                set_message("⚠️ Energia insuficiente para comprar animal.")
                return
            if fazenda.dinheiro < preco:
                set_message(f"💸 Dinheiro insuficiente. {a.nome} custa R$ {preco}.")
                return
            fazenda.adicionar_animal(a)
            set_message(f"🐾 Comprou {a.nome} por R$ {preco}.")
            atualizar_ui_all()
            if parent_panel: parent_panel.destroy()

        # ---------- Mercadinho ----------
        def abrir_mercadinho_panel():
            panel = tk.Toplevel(root)
            panel.title("Mercadinho")
            panel.configure(bg=THEME_BG)
            panel.geometry("420x360")
            tk.Label(panel, text="🛒 Mercadinho", bg=THEME_BG, font=(None,12,'bold')).pack(pady=8)
            itens = [('Ração para Animais 🥣',8,'racao'),('Pesticida 🧴',10,'protecao')]
            if fazenda.nivel >= 4: itens.append(('Arroz 🍚',10,'ingrediente'))
            for nome, preco, tipo in itens:
                def cmd(n=nome,p=preco,t=tipo):
                    if not fazenda.gastar_energia(1):
                        set_message("⚠️ Energia insuficiente para comprar."); return
                    if fazenda.dinheiro < p:
                        set_message(f"💸 Dinheiro insuficiente. {n} custa R$ {p}."); return
                    fazenda.dinheiro -= p
                    if t == 'racao':
                        fazenda.racao += 1
                    elif t == 'protecao':
                        fazenda.protecao = True
                    else:
                        fazenda.estoque.append({'nome': n.replace(' 🍚',''), 'preco': p})
                        fazenda.status_estoque.append(n.replace(' 🍚',''))

                    salvar_fazenda(fazenda)
                    set_message(f"🛒 Comprou {n} por R$ {p}.")
                    atualizar_ui_all()
                b = tk.Button(panel, text=f"{nome} — R$ {preco}", bg=BTN, width=36, command=cmd)
                b.pack(pady=6)

        # ---------- Fábrica ----------
        def abrir_fabrica_panel():
            if fazenda.nivel < 3:
                set_message("🏭 Fábrica desbloqueada no nível 3."); return
            fwin = tk.Toplevel(root); fwin.title('Fábrica'); fwin.configure(bg=THEME_BG)
            tk.Label(fwin, text='🏭 Fábrica', bg=THEME_BG, font=(None,12,'bold')).pack(pady=6)
            opc = [
                ('🧀 Queijo (2 Leites)', 'Queijo', [('Leite',2)], 25),
                ('🧈 Manteiga (3 Leites)', 'Manteiga', [('Leite',3)], 40),
                ('🧶 Suéter (3 Lãs)', 'Suéter', [('Lã',3)], 60)
            ]
            for label, nome, reqs, preco in opc:
                def cmd(nm=nome, r=reqs, p=preco):
                    ok = True
                    for rn, q in r:
                        cnt = sum(1 for it in fazenda.estoque if it.get('nome') == rn)
                        if cnt < q: ok = False
                    if not ok:
                        set_message("❌ Ingredientes insuficientes."); return
                    for rn, q in r:
                        removed = 0
                        for it in list(fazenda.estoque):
                            if it.get('nome') == rn and removed < q:
                                fazenda.estoque.remove(it); removed += 1
                                try: fazenda.status_estoque.remove(rn)
                                except: pass
                    fazenda.estoque.append({'nome': nm, 'preco': p}); fazenda.status_estoque.append(nm)
                    set_message(f"✅ Fabricou {nm}.")
                    atualizar_ui_all()
                b = tk.Button(fwin, text=f"{label}", bg=BTN, width=44, command=cmd)
                b.pack(pady=6)

        # ---------- Lagoa ----------
        def lagoa_pesca():
            if fazenda.nivel < 4: set_message("🎣 Lagoa desbloqueada no nível 4."); return
            if not fazenda.gastar_energia(3): set_message("⚠️ Energia insuficiente para pescar (3)."); return
            if random.random() < 0.2: set_message("💨 O peixe escapou..."); return
            tipo = random.choices(['Peixe Comum','Peixe Raro'], weights=[0.8,0.2])[0]
            precos = {'Peixe Comum':10,'Peixe Raro':30}
            fazenda.estoque.append({'nome':tipo,'preco':precos[tipo]}); fazenda.status_estoque.append(tipo)
            set_message(f"🐟 Você pescou: {tipo}.")
            atualizar_ui_all()

        # ---------- Ações ----------
        def acao_crescer():
            if not fazenda.plantas:
                set_message("🌱 Não há plantas para crescer.")
                return
            fazenda.crescendo()  
            set_message("🌿 Plantas atualizadas.")
            atualizar_ui_all()

        def acao_colher():
            if not fazenda.plantas:
                set_message("⚠️ Não há plantas para colher.")
                return
            fazenda.colher()  
            set_message("🌾 Colheita realizada — produtos adicionados ao estoque.")
            atualizar_ui_all()

        def acao_alimentar():
            if not fazenda.animais:
                set_message("⚠️ Não há animais para alimentar."); return
            if fazenda.racao <= 0:
                set_message("⚠️ Sem ração. Compre no mercadinho."); return
            if not fazenda.gastar_energia(1): set_message("⚠️ Energia insuficiente para alimentar animais."); return
            fazenda.alimentar_animais()
            fazenda.racao -= 1
            salvar_fazenda(fazenda)
            set_message("🐄 Animais alimentados; produtos (se gerados) foram para o estoque.")
            atualizar_ui_all()

        def encerrar_dia():
            perdidas = fazenda.encerra_dia()  
            salvar_fazenda(fazenda)  

            if perdidas:
                messagebox.showwarning("🐛 Ataque de pragas!", f"As pragas destruíram: {', '.join(perdidas)}")
            elif fazenda.protecao:
                messagebox.showinfo("🛡️ Pesticida", "O pesticida protegeu suas plantações hoje!")
            else:
                messagebox.showinfo("🌙 Fim do dia", "Dia encerrado. Energia restaurada.")

            set_message("🌙 Dia encerrado. Energia restaurada.")
            atualizar_ui_all()

        # ---------- Vendas ----------
        def vender_selecionado(lb, msg_var):
            sel = lb.curselection()
            if not sel:
                set_message("Selecione um item no estoque para vender."); return
            idx = sel[0]
            texto = lb.get(idx)
            if ' - R$ ' in texto:
                nome = texto.split(' - R$ ')[0].strip()
                try:
                    preco = float(texto.split(' - R$ ')[1])
                except:
                    set_message("Erro ao interpretar o preço."); return
            else:
                set_message("Erro ao interpretar o item."); return
            for it in fazenda.estoque:
                display = f"{emoji(it.get('nome'))} {it.get('nome')} - R$ {it.get('preco')}"
                if display.startswith(nome) or it.get('nome') in nome:
                    fazenda.dinheiro += it.get('preco',0)
                    fazenda.estoque.remove(it)
                    try: fazenda.status_estoque.remove(it.get('nome'))
                    except: pass
                    set_message(f"💵 Vendeu {it.get('nome')} por R$ {it.get('preco')}.")
                    atualizar_ui_all()
                    return
            set_message("✅ Venda realizada.")
            atualizar_ui_all()

        def vender_tudo(msg_var):
            if not fazenda.estoque:
                set_message("Estoque vazio."); return
            total = sum(i['preco'] for i in fazenda.estoque)
            if not fazenda.gastar_energia(1):
                set_message("⚠️ Energia insuficiente para vender."); return
            fazenda.dinheiro += total
            fazenda.estoque.clear(); fazenda.status_estoque.clear()
            set_message(f"💰 Vendeu tudo por R$ {total:.2f}.")
            atualizar_ui_all()

        # ---------- Botões principais ----------
        btns_info = [
            ("🛒 Mercadinho", abrir_mercadinho_panel),
            ("🏪 Comprar", abrir_loja_panel),
            ("🌱 Crescer Plantas", acao_crescer),
            ("🍽️ Alimentar Animais", acao_alimentar),
            ("🌾 Colher", acao_colher),
            ("🏭 Fábrica", abrir_fabrica_panel),
            ("🎣 Lagoa (Pescar)", lagoa_pesca),
            ("🛎️ Encerrar Dia", encerrar_dia)
        ]
        for text, fn in btns_info:
            b = tk.Button(actions, text=text, bg=BTN, width=28, height=2, command=fn)
            b.pack(pady=6)

        atualizar_ui_all()


    if fazenda is None:
        show_welcome()
    else:
        try:
            fazenda.energia_maxima = fazenda.calcular_energia_maxima()
            fazenda.energia = min(fazenda.energia, fazenda.energia_maxima)
        except Exception:
            pass
        show_main()

    def on_close_all():
        try:
            salvar_fazenda(fazenda)
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close_all)
    root.mainloop()


if __name__ == "__main__":
    abrir_interface_jogo()

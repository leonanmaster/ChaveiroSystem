import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog  
import pandas as pd                              
from datetime import datetime                   
from src.controllers import ProdutoController, CaixaController


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestão Chaveiro 1.0")
        self.geometry("900x600")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe")
        
        self.label_titulo = ctk.CTkLabel(self.frame_menu, text="CHAVEIRO\nSYSTEM", 
                                         font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.grid(row=0, column=0, padx=20, pady=20)

        self.btn_estoque = ctk.CTkButton(self.frame_menu, text="📦 Estoque", 
                                         command=lambda: self.mostrar_tela("estoque"))
        self.btn_estoque.grid(row=1, column=0, padx=20, pady=10)

        self.btn_vendas = ctk.CTkButton(self.frame_menu, text="💰 Caixa / Vendas", 
                                        command=lambda: self.mostrar_tela("vendas"))
        self.btn_vendas.grid(row=2, column=0, padx=20, pady=10)

        self.btn_servicos = ctk.CTkButton(self.frame_menu, text="🛠️ Serviços", 
                                          command=lambda: self.mostrar_tela("servicos"))
        self.btn_servicos.grid(row=3, column=0, padx=20, pady=10)

        self.btn_relat = ctk.CTkButton(self.frame_menu, text="📊 Relatórios", 
                                       command=lambda: self.mostrar_tela("relatorios"))
        self.btn_relat.grid(row=4, column=0, padx=20, pady=10)

        self.frame_conteudo = ctk.CTkFrame(self)
        self.frame_conteudo.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.tela_estoque = FrameEstoque(self.frame_conteudo)
        self.tela_vendas = FrameVendas(self.frame_conteudo)
        self.tela_relatorios = FrameRelatorios(self.frame_conteudo)
        self.tela_servicos = FrameServicos(self.frame_conteudo)

        self.mostrar_tela("estoque")
    
    def mostrar_tela(self, nome_tela):
        self.tela_estoque.pack_forget()
        self.tela_vendas.pack_forget()
        self.tela_servicos.pack_forget() 
        self.tela_relatorios.pack_forget()

        if nome_tela == "estoque":
            self.tela_estoque.pack(fill="both", expand=True)
            self.tela_estoque.listar_produtos()
            
        elif nome_tela == "vendas":
            self.tela_vendas.pack(fill="both", expand=True)
            self.tela_vendas.atualizar_lista_produtos()
            
        elif nome_tela == "servicos":        
            self.tela_servicos.pack(fill="both", expand=True)
            
        elif nome_tela == "relatorios":
            self.tela_relatorios.pack(fill="both", expand=True)

from tkinter import messagebox 

class FrameEstoque(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = ProdutoController()
        
        self.produto_selecionado_id = None
        self.produto_selecionado_nome = None

        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.frame_novo = ctk.CTkFrame(self)
        self.frame_novo.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_novo, text="Novo Produto:").pack(side="left", padx=5)
        
        self.entry_nome = ctk.CTkEntry(self.frame_novo, placeholder_text="Nome", width=180)
        self.entry_nome.pack(side="left", padx=5)
        
        self.entry_valor = ctk.CTkEntry(self.frame_novo, placeholder_text="Preço Venda", width=100)
        self.entry_valor.pack(side="left", padx=5)
        
        self.entry_qtd = ctk.CTkEntry(self.frame_novo, placeholder_text="Qtd", width=60)
        self.entry_qtd.pack(side="left", padx=5)

        self.entry_custo_ini = ctk.CTkEntry(self.frame_novo, placeholder_text="Custo Total (R$)", width=110)
        self.entry_custo_ini.pack(side="left", padx=5)

        self.btn_salvar = ctk.CTkButton(self.frame_novo, text="Salvar", command=self.adicionar_produto, fg_color="green", width=80)
        self.btn_salvar.pack(side="left", padx=10)

        self.lbl_msg = ctk.CTkLabel(self.frame_novo, text="", text_color="gray")
        self.lbl_msg.pack(side="left", padx=5)

        self.frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_acoes.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        self.lbl_selecionado = ctk.CTkLabel(self.frame_acoes, text="Selecione na tabela para ações", text_color="gray")
        self.lbl_selecionado.pack(side="left", padx=5)

        self.entry_repor_qtd = ctk.CTkEntry(self.frame_acoes, placeholder_text="Qtd +", width=60)
        self.entry_repor_qtd.pack(side="left", padx=5)
        
        self.entry_custo_total = ctk.CTkEntry(self.frame_acoes, placeholder_text="Custo Reposição (R$)", width=140)
        self.entry_custo_total.pack(side="left", padx=5)
        
        self.btn_repor = ctk.CTkButton(self.frame_acoes, text="Confirmar Entrada", command=self.repor_estoque, state="disabled", width=120)
        self.btn_repor.pack(side="left", padx=5)

        self.btn_excluir = ctk.CTkButton(self.frame_acoes, text="Excluir 🗑️", command=self.excluir_produto, 
                                         state="disabled", fg_color="red", hover_color="#8B0000", width=100)
        self.btn_excluir.pack(side="right", padx=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", bordercolor="#2b2b2b")
        style.map('Treeview', background=[('selected', '#1f538d')])

        colunas = ("ID", "Nome", "Valor", "Estoque")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="PRODUTO")
        self.tree.heading("Valor", text="PREÇO")
        self.tree.heading("Estoque", text="QTD")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=300)
        self.tree.column("Valor", width=100, anchor="center")
        self.tree.column("Estoque", width=100, anchor="center")

        self.tree.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_produto)
        
        self.scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=1, sticky="ns")

        self.listar_produtos()

    def ao_selecionar_produto(self, event):
        selection = self.tree.selection()
        if not selection: return
        
        item = self.tree.item(selection[0])
        dados = item['values']
        self.produto_selecionado_id = dados[0]
        self.produto_selecionado_nome = dados[1]
        
        self.lbl_selecionado.configure(text=f"Selecionado: {self.produto_selecionado_nome}", text_color="white")
        self.btn_repor.configure(state="normal", fg_color="#1f538d")
        self.btn_excluir.configure(state="normal")

    def excluir_produto(self):
        if not self.produto_selecionado_id: return
        if messagebox.askyesno("Confirmar", f"Apagar '{self.produto_selecionado_nome}'?"):
            self.controller.deletar(self.produto_selecionado_id)
            self.listar_produtos()
            self.lbl_selecionado.configure(text="Produto removido.", text_color="orange")
            self.btn_repor.configure(state="disabled")
            self.btn_excluir.configure(state="disabled")
            self.produto_selecionado_id = None

    def adicionar_produto(self):
        try:
            nome = self.entry_nome.get()
            if not nome:
                self.lbl_msg.configure(text="Nome obrigatório", text_color="red")
                return

            val_str = self.entry_valor.get().replace(",", ".")
            if not val_str: raise ValueError
            valor = float(val_str)
            
            qtd_str = self.entry_qtd.get()
            qtd = int(qtd_str) if qtd_str else 0
            
            custo_str = self.entry_custo_ini.get().replace(",", ".")
            custo_inicial = float(custo_str) if custo_str else 0.0

            if self.controller.buscar_por_nome(nome):
                self.lbl_msg.configure(text=f"Erro: '{nome}' já existe!", text_color="red")
                return

            self.controller.cadastrar(nome, valor, qtd, custo_inicial)
            
            self.entry_nome.delete(0, 'end')
            self.entry_valor.delete(0, 'end')
            self.entry_qtd.delete(0, 'end')
            self.entry_custo_ini.delete(0, 'end')
            
            self.listar_produtos()
            self.lbl_msg.configure(text="Cadastrado!", text_color="green")
            
        except ValueError:
            self.lbl_msg.configure(text="Erro nos valores", text_color="red")

    def repor_estoque(self):
        if not self.produto_selecionado_id: return
        try:
            qtd = int(self.entry_repor_qtd.get())
            
            custo_str = self.entry_custo_total.get().replace(",", ".")
            custo = float(custo_str) if custo_str else 0.0
            
            sucesso, msg = self.controller.repor_estoque(self.produto_selecionado_id, qtd, custo)
            
            if sucesso:
                self.listar_produtos()
                self.entry_repor_qtd.delete(0, 'end')
                self.entry_custo_total.delete(0, 'end')
                self.lbl_selecionado.configure(text=msg, text_color="green")
            else:
                self.lbl_selecionado.configure(text=msg, text_color="red")
                
        except ValueError:
             self.lbl_selecionado.configure(text="Revise Qtd e Custo", text_color="red")

    def listar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        produtos = self.controller.listar_todos()
        for p in produtos:
            self.tree.insert("", "end", values=(p[0], p[1], f"R$ {p[2]:.2f}", p[3]))

class FrameVendas(ctk.CTkFrame):
    
    def __init__(self, master):
        super().__init__(master)
        
        self.produto_controller = ProdutoController()
        self.caixa_controller = CaixaController()
        self.carrinho = []
        
        self.lista_produtos_completa = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        
        ctk.CTkLabel(self.frame_form, text="NOVA VENDA", font=("Arial", 16, "bold")).pack(pady=10)
        
        ctk.CTkLabel(self.frame_form, text="🔍 Pesquisar (Nome ou ID):").pack(pady=(10, 0))
        self.entry_busca = ctk.CTkEntry(self.frame_form, placeholder_text="Digite para filtrar...")
        self.entry_busca.pack(pady=5)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_produtos)
        
        ctk.CTkLabel(self.frame_form, text="Selecionar Produto:").pack(pady=(10, 0))
        self.combo_produtos = ctk.CTkComboBox(self.frame_form, width=200)
        self.combo_produtos.set("Selecione...")
        self.combo_produtos.pack(pady=5)
        
        ctk.CTkLabel(self.frame_form, text="Quantidade:").pack(pady=(10, 0))
        self.entry_qtd = ctk.CTkEntry(self.frame_form, width=100, placeholder_text="1")
        self.entry_qtd.pack(pady=5)

        self.btn_add = ctk.CTkButton(self.frame_form, text="Adicionar ao Carrinho ⬇", 
                                     command=self.adicionar_item, fg_color="#1f538d")
        self.btn_add.pack(pady=20)

        self.btn_remover = ctk.CTkButton(self.frame_form, text="Remover Item 🗑️", 
                                         command=self.remover_item, fg_color="gray", state="disabled")
        self.btn_remover.pack(pady=10)

        self.frame_carrinho = ctk.CTkFrame(self)
        self.frame_carrinho.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        self.frame_carrinho.grid_rowconfigure(1, weight=1)
        self.frame_carrinho.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame_carrinho, text="CARRINHO", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10)

        colunas = ("Nome", "Valor Un.", "Qtd", "Subtotal")
        self.tree_carrinho = ttk.Treeview(self.frame_carrinho, columns=colunas, show="headings")
        self.tree_carrinho.heading("Nome", text="PRODUTO")
        self.tree_carrinho.heading("Valor Un.", text="PREÇO UN.")
        self.tree_carrinho.heading("Qtd", text="QTD")
        self.tree_carrinho.heading("Subtotal", text="TOTAL")
        
        self.tree_carrinho.column("Nome", width=200)
        self.tree_carrinho.column("Valor Un.", width=80, anchor="center")
        self.tree_carrinho.column("Qtd", width=50, anchor="center")
        self.tree_carrinho.column("Subtotal", width=80, anchor="center")
        
        self.tree_carrinho.grid(row=1, column=0, sticky="nswe", padx=10)
        self.tree_carrinho.bind("<<TreeviewSelect>>", self.ao_selecionar_carrinho)

        self.frame_total = ctk.CTkFrame(self.frame_carrinho, fg_color="#2b2b2b")
        self.frame_total.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        self.lbl_total = ctk.CTkLabel(self.frame_total, text="TOTAL: R$ 0.00", font=("Arial", 24, "bold"), text_color="#00FF00")
        self.lbl_total.pack(side="left", padx=20, pady=20)
        
        self.btn_finalizar = ctk.CTkButton(self.frame_total, text="CONCLUIR VENDA ✅", 
                                           command=self.finalizar_venda, fg_color="green", height=50, font=("Arial", 14, "bold"))
        self.btn_finalizar.pack(side="right", padx=20)

        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):
        produtos = self.produto_controller.listar_todos()
        self.lista_produtos_completa = [f"{p[0]} - {p[1]}" for p in produtos]
        
        self.combo_produtos.configure(values=self.lista_produtos_completa)
        self.combo_produtos.set("Selecione...")

    def filtrar_produtos(self, event):
        termo = self.entry_busca.get().lower()
        
        if termo == "":
            self.combo_produtos.configure(values=self.lista_produtos_completa)
            self.combo_produtos.set("Selecione...")
            return

        lista_filtrada = [
            item for item in self.lista_produtos_completa 
            if termo in item.lower()
        ]
        
        self.combo_produtos.configure(values=lista_filtrada)
        
        if lista_filtrada:
            self.combo_produtos.set(lista_filtrada[0])
        else:
            self.combo_produtos.set("Nenhum produto encontrado")

    def adicionar_item(self):
        selecao = self.combo_produtos.get()
        if not selecao or selecao == "Selecione..." or selecao == "Nenhum produto encontrado":
            return

        try:
            id_prod = int(selecao.split(" - ")[0])
            qtd_txt = self.entry_qtd.get()
            qtd_solicitada = int(qtd_txt) if qtd_txt else 1
            
            conn = self.produto_controller.db.conn
            cursor = conn.cursor()
            cursor.execute("SELECT nome, valor, estoque FROM produtos WHERE id = ?", (id_prod,))
            prod_dados = cursor.fetchone()
            
            if not prod_dados: return
            nome, valor, estoque_atual = prod_dados
            
            if estoque_atual < qtd_solicitada:
                messagebox.showerror("Estoque", f"Apenas {estoque_atual} unidades disponíveis!")
                return

            for item in self.carrinho:
                if item['id'] == id_prod:
                    if (item['qtd'] + qtd_solicitada) > estoque_atual:
                         messagebox.showerror("Estoque", "Limite de estoque atingido!")
                         return
                    item['qtd'] += qtd_solicitada
                    item['total'] = item['qtd'] * valor
                    self.renderizar_carrinho()
                    self.limpar_campos_apos_add()
                    return

            self.carrinho.append({
                'id': id_prod,
                'nome': nome,
                'valor': valor,
                'qtd': qtd_solicitada,
                'total': valor * qtd_solicitada
            })
            self.renderizar_carrinho()
            self.limpar_campos_apos_add()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")

    def limpar_campos_apos_add(self):
        self.entry_busca.delete(0, 'end')
        self.entry_qtd.delete(0, 'end')
        self.atualizar_lista_produtos() 
        self.entry_busca.focus()

    def renderizar_carrinho(self):
        for i in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(i)
        
        total_geral = 0.0
        for item in self.carrinho:
            self.tree_carrinho.insert("", "end", values=(
                item['nome'], 
                f"R$ {item['valor']:.2f}", 
                item['qtd'], 
                f"R$ {item['total']:.2f}"
            ))
            total_geral += item['total']
            
        self.lbl_total.configure(text=f"TOTAL: R$ {total_geral:.2f}")

    def ao_selecionar_carrinho(self, event):
        self.btn_remover.configure(state="normal")

    def remover_item(self):
        selecao = self.tree_carrinho.selection()
        if not selecao: return
        index = self.tree_carrinho.index(selecao[0])
        del self.carrinho[index]
        self.renderizar_carrinho()
        self.btn_remover.configure(state="disabled")

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showwarning("Vazio", "Adicione itens ao carrinho!")
            return
            
        if messagebox.askyesno("Confirmar", f"Finalizar venda de R$ {self.lbl_total.cget('text').split('R$ ')[1]}?"):
            dados = [(i['id'], i['qtd']) for i in self.carrinho]
            sucesso, msg = self.caixa_controller.realizar_venda_carrinho(dados)
            
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.carrinho = []
                self.renderizar_carrinho()
                self.atualizar_lista_produtos()
            else:
                messagebox.showerror("Erro", msg)

class FrameServicos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = CaixaController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_centro = ctk.CTkFrame(self)
        self.frame_centro.grid(row=0, column=0, padx=20, pady=20)

        ctk.CTkLabel(self.frame_centro, text="REGISTRAR SERVIÇO AVULSO", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.frame_centro, text="(Ex: Aberturas, Confecções, Mão de obra...)", text_color="gray").pack(pady=(0, 20))

        ctk.CTkLabel(self.frame_centro, text="Descrição do Serviço:").pack(anchor="w", padx=20)
        self.entry_desc = ctk.CTkEntry(self.frame_centro, placeholder_text="Ex: Abertura de Porta Residencial", width=350)
        self.entry_desc.pack(pady=5, padx=20)

        ctk.CTkLabel(self.frame_centro, text="Valor Cobrado (R$):").pack(anchor="w", padx=20, pady=(10,0))
        self.entry_valor = ctk.CTkEntry(self.frame_centro, placeholder_text="0.00", width=150)
        self.entry_valor.pack(pady=5, padx=20)

        self.btn_salvar = ctk.CTkButton(self.frame_centro, text="LANÇAR NO CAIXA 💰", 
                                        command=self.registrar, fg_color="#1f538d", height=40, width=200)
        self.btn_salvar.pack(pady=30)
        
        self.lbl_msg = ctk.CTkLabel(self.frame_centro, text="")
        self.lbl_msg.pack(pady=5)

    def registrar(self):
        desc = self.entry_desc.get()
        val_str = self.entry_valor.get().replace(",", ".")
        
        if not desc:
            self.lbl_msg.configure(text="Erro: Descrição obrigatória!", text_color="red")
            return
            
        try:
            valor = float(val_str)
            self.controller.registrar_servico(desc, valor)
            
            self.lbl_msg.configure(text=f"✅ Serviço '{desc}' registrado com sucesso!", text_color="green")
            self.entry_desc.delete(0, 'end')
            self.entry_valor.delete(0, 'end')
            
        except ValueError:
            self.lbl_msg.configure(text="Erro: Valor inválido!", text_color="red")

class FrameRelatorios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = CaixaController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.frame_topo = ctk.CTkFrame(self)
        self.frame_topo.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkLabel(self.frame_topo, text="Gerar Relatório de:").pack(side="left", padx=10)
        
        self.combo_mes = ctk.CTkComboBox(self.frame_topo, values=[str(i) for i in range(1, 13)], width=70)
        self.combo_mes.set(str(datetime.now().month))
        self.combo_mes.pack(side="left", padx=5)
        
        ctk.CTkLabel(self.frame_topo, text="/").pack(side="left")
        
        self.entry_ano = ctk.CTkEntry(self.frame_topo, width=70)
        self.entry_ano.insert(0, str(datetime.now().year))
        self.entry_ano.pack(side="left", padx=5)
        
        self.btn_gerar = ctk.CTkButton(self.frame_topo, text="Consultar 🔍", command=self.gerar_relatorio)
        self.btn_gerar.pack(side="left", padx=10)

        self.btn_exportar = ctk.CTkButton(self.frame_topo, text="Exportar Excel 📊", 
                                          command=self.exportar_excel, fg_color="green", state="disabled")
        self.btn_exportar.pack(side="right", padx=10)

        self.frame_resumo = ctk.CTkFrame(self)
        self.frame_resumo.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.frame_resumo.grid_columnconfigure((0,1,2), weight=1)
        
        self.lbl_entradas = ctk.CTkLabel(self.frame_resumo, text="Entradas: R$ 0.00", 
                                         font=("Arial", 16), text_color="#00FF00")
        self.lbl_entradas.grid(row=0, column=0, pady=10)
        
        self.lbl_saidas = ctk.CTkLabel(self.frame_resumo, text="Despesas: R$ 0.00", 
                                       font=("Arial", 16), text_color="#FF4444")
        self.lbl_saidas.grid(row=0, column=1, pady=10)
        
        self.lbl_saldo = ctk.CTkLabel(self.frame_resumo, text="Lucro: R$ 0.00", 
                                      font=("Arial", 18, "bold"))
        self.lbl_saldo.grid(row=0, column=2, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", bordercolor="#2b2b2b")
        
        colunas = ("Data", "Tipo", "Descrição", "Valor")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        
        self.tree.heading("Data", text="DATA/HORA")
        self.tree.heading("Tipo", text="TIPO")
        self.tree.heading("Descrição", text="DESCRIÇÃO")
        self.tree.heading("Valor", text="VALOR")
        
        self.tree.column("Data", width=150, anchor="center")
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("Descrição", width=400)
        self.tree.column("Valor", width=100, anchor="center")
        
        self.tree.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
        
        self.df_atual = None

    def gerar_relatorio(self):
        try:
            mes = int(self.combo_mes.get())
            ano = int(self.entry_ano.get())
            
            self.df_atual = self.controller.buscar_relatorio_mensal(mes, ano)
            
            for i in self.tree.get_children():
                self.tree.delete(i)
                
            if self.df_atual.empty:
                messagebox.showinfo("Aviso", "Nenhuma movimentação neste período.")
                self.atualizar_resumo(0, 0, 0)
                self.btn_exportar.configure(state="disabled")
                return

            entradas = 0.0
            saidas = 0.0
            
            for index, row in self.df_atual.iterrows():
                data_formatada = pd.to_datetime(row['data_hora']).strftime('%d/%m/%Y %H:%M')
                val = row['valor']
                
                if val >= 0:
                    entradas += val
                else:
                    saidas += abs(val)
                
                self.tree.insert("", "end", values=(
                    data_formatada, 
                    row['tipo'], 
                    row['descricao'], 
                    f"R$ {val:.2f}"
                ))
            
            self.atualizar_resumo(entradas, saidas, entradas - saidas)
            self.btn_exportar.configure(state="normal")
            
        except ValueError:
            messagebox.showerror("Erro", "Ano inválido.")

    def atualizar_resumo(self, ent, sai, saldo):
        self.lbl_entradas.configure(text=f"Entradas: R$ {ent:.2f}")
        self.lbl_saidas.configure(text=f"Despesas: R$ {sai:.2f}")
        
        self.lbl_saldo.configure(text=f"Resultado: R$ {saldo:.2f}")
        if saldo >= 0:
            self.lbl_saldo.configure(text_color="#00FF00")
        else:
            self.lbl_saldo.configure(text_color="#FF4444")

    def exportar_excel(self):
        if self.df_atual is None or self.df_atual.empty:
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Salvar Relatório"
        )
        
        if filename:
            try:
                self.df_atual.to_excel(filename, index=False)
                messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")
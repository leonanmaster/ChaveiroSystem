from src.database import Database
from datetime import datetime
import pandas as pd

class ProdutoController:
    def __init__(self):
        self.db = Database()

    def cadastrar(self, nome, valor, estoque, custo_aquisicao=0):
        self.db.executar("INSERT INTO produtos (nome, valor, estoque) VALUES (?, ?, ?)", (nome, valor, estoque))

        if custo_aquisicao > 0:
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            desc = f"Estoque Inicial: {estoque}x {nome}"
            self.db.executar("INSERT INTO caixa (tipo, descricao, valor, data_hora) VALUES (?, ?, ?, ?)", 
                             ('COMPRA', desc, -abs(custo_aquisicao), agora))

    def listar_todos(self):
        sql = "SELECT * FROM produtos"
        cursor = self.db.executar(sql)
        return cursor.fetchall()

    def buscar_por_nome(self, nome):
        sql = "SELECT * FROM produtos WHERE nome = ?"
        cursor = self.db.executar(sql, (nome,))
        return cursor.fetchone()

    def atualizar(self, id_prod, novo_valor, novo_estoque):
        if novo_valor:
            self.db.executar("UPDATE produtos SET valor = ? WHERE id = ?", (novo_valor, id_prod))
        if novo_estoque:
            self.db.executar("UPDATE produtos SET estoque = ? WHERE id = ?", (novo_estoque, id_prod))

    def deletar(self, id_prod):
        self.db.executar("DELETE FROM produtos WHERE id = ?", (id_prod,))

    def repor_estoque(self, id_prod, qtd_nova, custo_total=0):
        cursor = self.db.executar("SELECT nome, estoque FROM produtos WHERE id = ?", (id_prod,))
        dados = cursor.fetchone()
        if not dados:
            return False, "Produto não encontrado."
            
        nome, estoque_atual = dados
        novo_estoque = estoque_atual + qtd_nova
        
        self.db.executar("UPDATE produtos SET estoque = ? WHERE id = ?", (novo_estoque, id_prod))
        
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        valor_registro = -abs(custo_total) if custo_total > 0 else 0
        desc = f"Reposição: {qtd_nova}x {nome}"
        
        self.db.executar("INSERT INTO caixa (tipo, descricao, valor, data_hora) VALUES (?, ?, ?, ?)", 
                         ('COMPRA', desc, valor_registro, agora))
                         
        return True, f"Estoque atualizado! Novo total: {novo_estoque}"


class CaixaController:
    def __init__(self):
        self.db = Database()

    def registrar_servico(self, descricao, valor):
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO caixa (tipo, descricao, valor, data_hora) VALUES (?, ?, ?, ?)"
        self.db.executar(sql, ('SERVICO', descricao, valor, agora))

    def realizar_venda_carrinho(self, itens_carrinho):
        try:
            total_venda = 0
            descricao_venda = "Venda: "
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for id_prod, qtd_venda in itens_carrinho:
                sql = "SELECT nome, valor, estoque FROM produtos WHERE id = ?"
                cursor = self.db.executar(sql, (id_prod,))
                produto = cursor.fetchone()
                
                if not produto: return False, f"ID {id_prod} erro."
                nome, valor, estoque = produto
                if estoque < qtd_venda: return False, f"Sem estoque de {nome}."

            for id_prod, qtd_venda in itens_carrinho:
                cursor = self.db.executar("SELECT nome, valor, estoque FROM produtos WHERE id = ?", (id_prod,))
                nome, valor, estoque_atual = cursor.fetchone()
                
                novo_estoque = estoque_atual - qtd_venda
                self.db.executar("UPDATE produtos SET estoque = ? WHERE id = ?", (novo_estoque, id_prod))
                
                total_venda += (valor * qtd_venda)
                descricao_venda += f"[{qtd_venda}x {nome}] "

            self.db.executar("INSERT INTO caixa (tipo, descricao, valor, data_hora) VALUES (?, ?, ?, ?)", 
                             ('VENDA', descricao_venda, total_venda, agora))
            
            return True, f"Venda R$ {total_venda:.2f} realizada!"

        except Exception as e:
            print(f"Erro: {e}")
            return False, "Erro interno."

    def buscar_relatorio_mensal(self, mes, ano):
        data_inicio = f"{ano}-{mes:02d}-01"
        if mes == 12:
            data_fim = f"{ano+1}-01-01"
        else:
            data_fim = f"{ano}-{mes+1:02d}-01"
            
        sql = """
            SELECT data_hora, tipo, descricao, valor 
            FROM caixa 
            WHERE data_hora >= ? AND data_hora < ?
            ORDER BY data_hora DESC
        """
        try:
            df = pd.read_sql_query(sql, self.db.conn, params=(data_inicio, data_fim))
            return df
        except Exception as e:
            print(f"Erro Pandas: {e}")
            return pd.DataFrame()
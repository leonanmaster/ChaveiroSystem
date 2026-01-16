import sqlite3
import os

class Database:
    def  __init__ (self, db_name="chaveiro.db"):
        os.makedirs('data', exist_ok=True)
        self.db_path = os.path.join('data', db_name)
        self.conn = None
        self.iniciar_conexao()
        self.criar_tabelas()
    
    def iniciar_conexao(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL,
                estoque INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def executar(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Erro no Banco: {e}")
            return None
    
    def fechar(self):
        if self.conn:
            self.conn.close()
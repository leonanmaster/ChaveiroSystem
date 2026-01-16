# 🔐 Chaveiro System - Sistema de Gestão para Chaveiros

> Sistema Desktop completo para controle de estoque, vendas e fluxo de caixa, desenvolvido com foco em arquitetura MVC e análise de dados.

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📄 Sobre o Projeto

Este projeto foi desenvolvido para atender a necessidade de pequenos negócios (focado em chaveiros) que precisam sair do papel/planilha e ter um controle real de seus lucros. 

Diferente de sistemas genéricos, ele possui fluxos específicos para **Produtos** (controle de estoque físico) e **Serviços** (mão de obra intangível), unificando tudo em relatórios financeiros precisos.

O software foi construído seguindo o padrão de arquitetura **MVC (Model-View-Controller)**, garantindo um código limpo, escalável e fácil de manter.

## ✨ Funcionalidades Principais

### 📦 Gestão de Estoque Inteligente
- **CRUD Completo:** Cadastro, leitura, atualização e exclusão de produtos.
- **Custo de Aquisição:** Registro do custo inicial e de reposição para cálculo real de lucro.
- **Reposição de Estoque:** Entrada de mercadoria gera automaticamente uma despesa no caixa.

### 💰 Frente de Caixa (PDV)
- **Busca Dinâmica:** Filtro em tempo real por Nome ou ID do produto.
- **Carrinho de Compras:** Adição de múltiplos itens antes de finalizar a venda.
- **Validação de Estoque:** O sistema impede vendas acima da quantidade disponível.
- **Baixa Automática:** Atualiza o banco de dados instantaneamente após a venda.

### 🛠️ Módulo de Serviços
- Registro de serviços avulsos (Ex: Aberturas, Confecções, Visitas Técnicas).
- Entrada direta no fluxo de caixa como receita de serviço.

### 📊 Business Intelligence (Relatórios)
- **Filtro Temporal:** Geração de relatórios por Mês e Ano.
- **Indicadores Visuais:** Cores dinâmicas para Lucro (Verde) e Prejuízo (Vermelho).
- **Análise de Dados:** Utilização da biblioteca **Pandas** para processamento dos dados.
- **Exportação:** Botão para gerar planilha Excel (`.xlsx`) detalhada com um clique.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3](https://www.python.org/)
- **Interface Gráfica (GUI):** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Visual moderno e Dark Mode nativo)
- **Banco de Dados:** SQLite3 (Nativo, sem necessidade de servidor)
- **Análise de Dados:** Pandas
- **Arquitetura:** MVC

## 🚀 Como rodar o projeto localmente

### Pré-requisitos
Certifique-se de ter o **Python 3.10+** e o **Git** instalados.

```bash
# 1. Clone o repositório
git clone [https://github.com/leonanmaster/ChaveiroSystem.git]

# 2. Entre na pasta do projeto
cd GestaoChaveiro

# 3. Crie um ambiente virtual (Recomendado)
python3 -m venv venv

# 4. Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# 5. Instale as dependências
pip install -r requirements.txt

# 6. Execute a aplicação
python3 main.py
```

## 📦 Como gerar o Executável (.exe ou binário)

Se deseja utilizar o software sem precisar do Python instalado:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter --name="KeyMaster" main.py
```
O arquivo executável estará na pasta `dist/`.

## 📂 Estrutura do Projeto

```
GestaoChaveiro/
├── src/
│   ├── __init__.py
│   ├── controllers.py   # Lógica de Negócio
│   ├── database.py      # Conexão e Queries SQL
│   └── view.py          # Interface Gráfica (Frontend Desktop)
├── data/                # Banco de dados SQLite (gerado automaticamente)
├── main.py              # Ponto de entrada
├── requirements.txt     # Lista de bibliotecas
└── README.md            # Documentação
```

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📝 Licença

Este projeto está sob a licença MIT.

---
Desenvolvido por Leonan Levy Nascimento Louvem - Estudante de Ciência da Computação (UFRRJ)

import tkinter as tk
from tkinter import messagebox, filedialog

class CalculadoraFinanceira:
    def __init__(self):
        self.receitas = []  # Lista de tuplas (nome, valor)
        self.despesas = []  # Lista de tuplas (nome, valor)

    def adicionar_receita(self, nome, valor):
        self.receitas.append((nome, valor))

    def adicionar_despesa(self, nome, valor):
        self.despesas.append((nome, valor))

    def calcular_saldo(self):
        return sum(valor for _, valor in self.receitas) - sum(valor for _, valor in self.despesas)

    def limpar_historico(self):
        self.receitas.clear()
        self.despesas.clear()

    def salvar_dados(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'w') as arquivo:
                arquivo.write("Receitas:\n")
                for nome, valor in self.receitas:
                    arquivo.write(f"{nome}: {valor}\n")
                arquivo.write("\nDespesas:\n")
                for nome, valor in self.despesas:
                    arquivo.write(f"{nome}: {valor}\n")
            return True, None
        except Exception as e:
            return False, str(e)

    def carregar_dados(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r') as arquivo:
                self.receitas.clear()
                self.despesas.clear()
                linhas = arquivo.readlines()
                secao = None
                for linha in linhas:
                    linha = linha.strip()
                    if linha == "Receitas:":
                        secao = "receitas"
                    elif linha == "Despesas:":
                        secao = "despesas"
                    elif linha and secao:
                        nome, valor = linha.split(": ")
                        valor = float(valor)
                        if secao == "receitas":
                            self.receitas.append((nome, valor))
                        elif secao == "despesas":
                            self.despesas.append((nome, valor))
        except Exception as e:
            raise ValueError(f"Erro ao carregar o arquivo: {e}")


# Funções para a interface gráfica
def adicionar_receita():
    nome = entry_nome.get()
    try:
        valor = float(entry_valor.get())
        calc.adicionar_receita(nome, valor)
        atualizar_saldo()
        atualizar_historico()
        entry_nome.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")


def adicionar_despesa():
    nome = entry_nome.get()
    try:
        valor = float(entry_valor.get())
        calc.adicionar_despesa(nome, valor)
        atualizar_saldo()
        atualizar_historico()
        entry_nome.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")


def atualizar_saldo():
    saldo = calc.calcular_saldo()
    lbl_saldo["text"] = f"Saldo: R$ {saldo:.2f}"


def atualizar_historico():
    historico = "Receitas:\n"
    for nome, valor in calc.receitas:
        historico += f"- {nome}: R$ {valor:.2f}\n"
    historico += "\nDespesas:\n"
    for nome, valor in calc.despesas:
        historico += f"- {nome}: R$ {valor:.2f}\n"
    txt_historico.delete(1.0, tk.END)
    txt_historico.insert(tk.END, historico)


def salvar_dados():
    caminho_arquivo = filedialog.asksaveasfilename(
        title="Salvar Arquivo",
        defaultextension=".txt",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if caminho_arquivo:
        sucesso, erro = calc.salvar_dados(caminho_arquivo)
        if sucesso:
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {erro}")


def carregar_dados():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=(("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*"))
    )
    if caminho_arquivo:
        try:
            calc.carregar_dados(caminho_arquivo)
            atualizar_saldo()
            atualizar_historico()
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar os dados: {e}")


def limpar_historico():
    if messagebox.askyesno("Confirmação", "Deseja realmente limpar todo o histórico?"):
        calc.limpar_historico()
        atualizar_saldo()
        atualizar_historico()


# Interface gráfica principal
calc = CalculadoraFinanceira()

root = tk.Tk()
root.title("Calculadora Financeira Pessoal")

# Entrada de nome e valor
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Valor:").grid(row=1, column=0, padx=5, pady=5)
entry_valor = tk.Entry(root)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

# Botões de receita e despesa
btn_receita = tk.Button(root, text="Adicionar Receita", command=adicionar_receita)
btn_receita.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
btn_despesa = tk.Button(root, text="Adicionar Despesa", command=adicionar_despesa)
btn_despesa.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Exibição do saldo
lbl_saldo = tk.Label(root, text="Saldo: R$ 0.00", font=("Arial", 16))
lbl_saldo.grid(row=3, column=0, columnspan=2, pady=10)

# Campo de histórico
txt_historico = tk.Text(root, width=40, height=15)
txt_historico.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Botões de salvar, carregar e limpar histórico
btn_salvar = tk.Button(root, text="Salvar Dados", command=salvar_dados)
btn_salvar.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
btn_carregar = tk.Button(root, text="Carregar Dados", command=carregar_dados)
btn_carregar.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
btn_limpar = tk.Button(root, text="Limpar Histórico", command=limpar_historico)
btn_limpar.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

root.mainloop()
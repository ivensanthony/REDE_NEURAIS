import customtkinter
import mysql.connector
from hashlib import sha256

class Cadastro:
    def __init__(self):
        self.conectar_interface()

    def conectar_banco(self):
        try:
            conexao = mysql.connector.connect(
                host='127.0.0.1',
                database='academy',
                user='root',
                password=''
            )
            return conexao
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return None

    def adicionar_usuario(self):
        email_val = self.email.get()
        senha_val = sha256(self.senha.get().encode()).hexdigest()  # Hash da senha
        conexao = self.conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO usuários (email, senha) VALUES (%s, %s)"
            cursor.execute(query, (email_val, senha_val))
            conexao.commit()
            print("Novo usuário adicionado com sucesso.")
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

    def autenticar_usuario(self):
        email_val = self.email.get()
        senha_val = sha256(self.senha.get().encode()).hexdigest()  # Hash da senha
        conexao = self.conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM usuários WHERE email = %s AND senha = %s"
            cursor.execute(query, (email_val, senha_val))
            result = cursor.fetchone()
            if result:
                print("Login bem-sucedido!")
            else:
                print("Email ou senha incorretos.")
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

    def conectar_interface(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        janela = customtkinter.CTk()
        janela.geometry("500x300")

        self.text = customtkinter.CTkLabel(janela, text="Fazer login")
        self.email = customtkinter.CTkEntry(janela, placeholder_text="email")
        self.senha = customtkinter.CTkEntry(janela, placeholder_text="senha", show="*")
        botao = customtkinter.CTkButton(janela, text="login", command=self.autenticar_usuario)
        botao_cadastro = customtkinter.CTkButton(janela, text="cadastrar", command=self.adicionar_usuario)

        self.text.pack(padx=10, pady=10)
        self.email.pack(padx=10, pady=10)
        self.senha.pack(padx=10, pady=10)
        botao.pack(padx=10, pady=10)
        botao_cadastro.pack(padx=10, pady=10)

        janela.mainloop()

if __name__ == "__main__":
    app = Cadastro()

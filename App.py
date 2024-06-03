import customtkinter
import mysql.connector
from mysql.connector import Error
try:
    # Conecta ao banco de dados
    conexao = mysql.connector.connect(
        host='127.0.0.1',
        database='academy',
        user='root',
        password=''
    )
    if conexao.is_connected():
        print("Conexão estabelecida!")
except Error as e:
    print(f"Erro ao conectar ao MySQL: {e}")
finally:
    if (conexao.is_connected()):
        conexao.close()
        print("Conexão encerrada.")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


janela = customtkinter.CTk()
janela.geometry("500x300")

def clique():
    print("Fazer login")

text = customtkinter.CTkLabel(janela, text="Fazer login")
email = customtkinter.CTkEntry(janela, placeholder_text="email")
senha = customtkinter.CTkEntry(janela,  placeholder_text="senha", show="*")
botao = customtkinter.CTkButton(janela, text="login", command= clique)



text.pack(padx=10, pady=10)
email.pack(padx=10, pady=10)
senha.pack(padx=10, pady=10)
botao.pack(padx=10, pady=10)


janela.mainloop()



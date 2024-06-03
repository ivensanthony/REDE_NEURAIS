import customtkinter
import mysql.connector

# Função para autenticar o usuário
def clique():
    email_val = email.get()
    senha_val = senha.get()
    
    # Conecta ao banco de dados
    conexao = mysql.connector.connect(
        host='127.0.0.1',
        database='academy',
        user='root',
        password=''
    )
    
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

# Configuração da interface gráfica
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()
janela.geometry("500x300")

text = customtkinter.CTkLabel(janela, text="Fazer login")
email = customtkinter.CTkEntry(janela, placeholder_text="email")
senha = customtkinter.CTkEntry(janela, placeholder_text="senha", show="*")
botao = customtkinter.CTkButton(janela, text="login", command=clique)

text.pack(padx=10, pady=10)
email.pack(padx=10, pady=10)
senha.pack(padx=10, pady=10)
botao.pack(padx=10, pady=10)

janela.mainloop()

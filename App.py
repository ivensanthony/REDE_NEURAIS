import customtkinter

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



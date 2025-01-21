from IA.Assistente import Assistente
import tkinter as tk
from tkinter import messagebox
import os

FILE_CONFIG_USER = "infor_user/config_user.json"
FILE_CONVERSA = "Conversas/conversa.txt"

def iniciar():
    # Create the root window to show the dialog box
    root = tk.Tk()
    root.withdraw()  # Hide the root window as we only need the dialog

    resp = messagebox.askyesno("Assistente", "Deseja iniciar o assistente sem janela?")
    if resp:
        print("Iniciando assistente sem janela")
        main()  # Directly call main without GUI
    else:
        print("Iniciando assistente com janela")

def conversa():
    if not os.path.exists(FILE_CONVERSA):
        #cria o arquivo
        arquivo = open(FILE_CONVERSA, "w")
        arquivo.close()
    arquivo = open(FILE_CONVERSA, "r")
    conversa = arquivo.read()
    return conversa

def salvar_conversa(conversa):
    arquivo = open(FILE_CONVERSA, "w")
    arquivo.write(conversa)
    arquivo.close()

def main():
    while True:
        pergunta = input("Digite sua pergunta: ")
        if pergunta == "sair":
            break
        pronpt = f"contexto:{conversa()}\nususario: {pergunta}"
        res = Assistente().resposta(pronpt)
        conversa_atual = conversa()
        conversa_atual += f"Usuário: {pergunta}\nAssistente: {res}\n"
        salvar_conversa(conversa_atual)
        print(res)
        print(pronpt)

if __name__ == "__main__":
    iniciar()
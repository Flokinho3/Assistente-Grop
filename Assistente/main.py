from IA.Assistente import Assistente
import tkinter as tk
from tkinter import messagebox
import os

# Constantes
FILE_CONFIG_USER = "infor_user/config_user.json"
FILE_CONVERSA = "Assistente/Conversas/conversa.txt"

def iniciar():
    """Inicia o assistente com ou sem janela."""
    # Cria a janela raiz para o diálogo
    root = tk.Tk()
    root.withdraw()  # Oculta a janela raiz

    # Exibe uma mensagem de diálogo para escolher o modo
    resp = messagebox.askyesno("Assistente", "Deseja iniciar o assistente sem janela?")
    if resp:
        print("Iniciando assistente sem janela")
        main()  # Executa o assistente diretamente no terminal
    else:
        print("Iniciando assistente com janela")

def conversa():
    """Lê o conteúdo do arquivo de conversas."""
    # Garante que o diretório e o arquivo existam
    os.makedirs(os.path.dirname(FILE_CONVERSA), exist_ok=True)
    if not os.path.exists(FILE_CONVERSA):
        with open(FILE_CONVERSA, "w") as arquivo:
            arquivo.write("")  # Cria um arquivo vazio
    
    # Lê o conteúdo do arquivo
    with open(FILE_CONVERSA, "r") as arquivo:
        return arquivo.read()

def salvar_conversa(conversa):
    """Salva a conversa atual no arquivo."""
    with open(FILE_CONVERSA, "w") as arquivo:
        arquivo.write(conversa)

def main():
    """Loop principal do assistente."""
    while True:
        pergunta = input("Digite sua pergunta: ")
        if pergunta.lower() == "sair":
            print("Encerrando o assistente...")
            break
        
        # Gera o prompt para o assistente
        prompt = f"contexto:{conversa()}\nusuário: {pergunta}"
        assistente = Assistente()
        res = assistente.resposta(prompt)
        
        # Atualiza e salva a conversa
        conversa_atual = conversa()
        conversa_atual += f"Usuário: {pergunta}\nAssistente: {res}\n"
        salvar_conversa(conversa_atual)

        # Exibe a resposta e o prompt
        print(f"Assistente: {res}")

if __name__ == "__main__":
    iniciar()

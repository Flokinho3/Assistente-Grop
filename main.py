import os
import json
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

FILE_DEPENDENCIAS = "Systema/Dependencias.json"
FILE_CONFIGURACOES = "Assistente/Configuracoes/key.txt"
FILE_MAIN = "Assistente/main.py"

# Carrega os dados do JSON
with open(FILE_DEPENDENCIAS, "r") as file:
    data = json.load(file)

def Verificar_caminho(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"Caminho {caminho} criado com sucesso.")
    else:
        print(f"Caminho {caminho} já existe.")

def salvar_link():
    if os.path.exists(data["FILES"][0]):
        with open(data["FILES"][0], "w") as file:
            file.write(data["link"])
    else:
        # Se não existir o arquivo link.txt, criamos ele
        with open(data["FILES"][0], "w") as file:
            file.write(data["link"])

def verificar_key():
    try:
        if os.path.exists(FILE_CONFIGURACOES):
            with open(FILE_CONFIGURACOES, "r") as file:
                key = file.read().strip()  # Remove espaços em branco
                if not key:  # Verifica se está vazio após remover espaços
                    print("Arquivo key.txt está vazio")
                    return False
                else:
                    return True
        else:
            print("Arquivo key.txt não existe")
            return False
    except Exception as e:
        print(f"Erro ao verificar key: {str(e)}")
        return False

def Criar_arquivos():
    for arquivo in data["FILES"]:
        # Obtém o diretório do arquivo
        diretorio = os.path.dirname(arquivo)
        # Verifica se o diretório existe, se não, cria
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        # Verifica se o arquivo já existe antes de criar ou sobrescrever
        if not os.path.exists(arquivo):
            with open(arquivo, "w") as file:
                file.write("")
    salvar_link()

def Criar_caminhos():
    for caminho in data["PATH"]:
        Verificar_caminho(caminho)

def verificar_instalacao(biblioteca):
    """
    Verifica se uma biblioteca está instalada. 
    Se não estiver, pergunta ao usuário se deseja instalar.
    """
    try:
        __import__(biblioteca)
        print(f"Biblioteca '{biblioteca}' já está instalada.")
    except ImportError:
        print(f"Biblioteca '{biblioteca}' não encontrada.")
        resposta = input(f"Deseja instalar '{biblioteca}' agora? (s/n): ").strip().lower()
        if resposta == 's':
            try:
                print(f"Instalando '{biblioteca}'...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", biblioteca])
                print(f"Biblioteca '{biblioteca}' instalada com sucesso!")
            except Exception as e:
                print(f"Erro ao instalar '{biblioteca}': {e}")
        else:
            print(f"Biblioteca '{biblioteca}' não será instalada.")
def Criar_bibliotecas():
    """
    Verifica e importa as bibliotecas listadas no JSON.
    Instala automaticamente as que não estiverem presentes.
    """
    bibliotecas_importadas = {}
    for biblioteca in data["BIBLIOTECAS"]:
        if biblioteca:  # Verifica se a biblioteca não está vazia
            try:
                bibliotecas_importadas[biblioteca] = __import__(biblioteca)
                print(f"Biblioteca {biblioteca} carregada com sucesso.")
            except ImportError:
                print(f"Biblioteca {biblioteca} não encontrada. Instalando...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", biblioteca])
                    bibliotecas_importadas[biblioteca] = __import__(biblioteca)
                    print(f"Biblioteca {biblioteca} instalada e carregada com sucesso.")
                except Exception as e:
                    print(f"Erro ao instalar a biblioteca {biblioteca}: {e}")
    return bibliotecas_importadas


# Função que chama as funções principais e exibe uma mensagem de sucesso
def Tutorial():
    """
    O tutorial explicará a preparação de arquivo key para o uso do assistente usando messagebox.
    """
    for tutorial in data["TUTORIAL"]:
        messagebox.showinfo("Tutorial", tutorial)

def Verificar():
    print("Verificando arquivos, caminhos e bibliotecas...")
    Criar_arquivos()
    Criar_caminhos()
    Criar_bibliotecas()
    
    if verificar_key():
        messagebox.showinfo("Verificação", "Arquivos, caminhos e bibliotecas verificados e criados com sucesso!")
        data["Execucao"] = False
    else:
        if not os.path.exists(FILE_CONFIGURACOES):
            messagebox.showinfo("Primeira Execução", "Arquivos e configurações iniciais criados com sucesso. Agora, crie o arquivo 'key.txt'.")
        else:
            messagebox.showerror("ATENÇÃO", "Key não encontrada, verifique se o arquivo key.txt existe no diretório Assistente/Configuracoes/")

def Iniciar():
    subprocess.run([sys.executable, FILE_MAIN])
    sys.exit()

def Sair():
    print("Saindo do assistente...")
    root.quit()

def Atualizar_Interface(botao_iniciar):
    """Função para habilitar/desabilitar o botão 'Iniciar'."""
    if verificar_key():  # Verifica se o arquivo "key.txt" existe
        botao_iniciar.config(state=tk.NORMAL)
    else:
        botao_iniciar.config(state=tk.DISABLED)

def inicio():
    global botao_executar, botao_iniciar, root
    root = tk.Tk()
    root.title("Assistente")
    root.geometry("300x200")
    root.resizable(False, False)
    root.configure(bg="black")

    # Criação do botão para executar as instruções iniciais
    botao_executar = tk.Button(root, text="Executar", command=Tutorial)
    botao_executar.pack(pady=10)

    # Criação do botão para verificar arquivos, caminhos e bibliotecas
    botao_verificar = tk.Button(root, text="Verificar", command=Verificar)
    botao_verificar.pack(pady=10)

    # Criação do botão para iniciar o assistente (inicialmente desativado)
    botao_iniciar = tk.Button(root, text="Iniciar", command=Iniciar)
    botao_iniciar.pack(pady=10)
    botao_iniciar.config(state=tk.DISABLED)

    # Criação do botão para sair
    botao_sair = tk.Button(root, text="Sair", command=Sair)
    botao_sair.pack(pady=10)

    # Atualiza o estado dos botões
    Atualizar_Interface(botao_iniciar)

    # Iniciar a interface gráfica
    root.mainloop()

# Chama a função que cria a interface gráfica
if __name__ == "__main__":
    Criar_caminhos()  # Garante que os diretórios existam
    Criar_arquivos()  # Garante que os arquivos existam
    Criar_bibliotecas()  # Verifica e instala as bibliotecas
    Verificar()  # Verifica arquivos e inicializa o sistema
    inicio()  # Inicia a interface


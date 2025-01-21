from groq import Groq
from tkinter import messagebox

FILE_KEY = "Assistente/Configuracoes/key.txt"

class Assistente:
    def __init__(self):
        self.api_key = None
        self.groq_api_key = None
        self.url = None
        self.payload = None
        self.header = None
        self.mensagem = None

    def load_key(self):
        try:
            with open(FILE_KEY, "r") as file:
                self.api_key = file.read().strip()
                if not self.api_key:
                    messagebox.showerror("Erro", "Arquivo key.txt está vazio!\nVamos tentar subir um nível.")
                    return False
                else:
                    return True
        except Exception as e:
            try:
                #tenta subir um nível
                with open("../" + FILE_KEY, "r") as file:
                    self.api_key = file.read().strip()
                    if not self.api_key:
                        messagebox.showerror("Erro", "Arquivo key.txt está vazio!\nFeche a aplicaçao e clique em 'Executar'.")
                        return False
                    else:
                        return True
            except Exception as e:
                messagebox.showerror("Erro", "Erro ao carregar chave de API.\n" + str(e))
            return False

    def resposta(self, text):
        if not self.load_key():  # Verifica se a chave foi carregada corretamente
            return "Erro ao carregar chave de API."

        client = Groq(api_key=self.api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        respsota = chat_completion.choices[0].message.content
        return respsota

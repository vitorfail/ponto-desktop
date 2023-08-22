import customtkinter as ctk
import tkinter.messagebox as tkmb
import tkinter as tk
import requests
import os
from api import server
import json
from cadastro_rosto import CadastroRosto 
from pathlib import Path
from treinamento import Treinamento
from reconhecimento import Reconhecimento
import threading

class PontoOnline():
	def __init__(self, root):
		self.variable_ready = threading.Event()
		self.appdata_path = os.getenv('APPDATA')
		self.texto_carregamento = "Aguarde estamos criando as pastas"
		self.root = root	
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		width = 400
		height = 400
		x_coordinate = (screen_width - width) // 2
		y_coordinate = (screen_height - height) // 2
		self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

		self.root.title("PONTO ONLINE")
		self.root.iconbitmap("icon.ico")
		self.lista = []
		

		self.ponto = ctk.CTkScrollableFrame(self.root)
		self.login = ctk.CTkFrame(self.root)
		self.aguarde = ctk.CTkFrame(self.root)

		self.current_frame = self.login
		self.show_frame()


		self.create_login()
		self.loading()
        
	def create_ponto(self):
		pasta_faces = os.path.join(self.appdata_path, "PontoLog\dataFace")
		file_path = os.path.join(self.appdata_path, "PontoLog\log.txt")
		ler = open(file_path, "r")
		linhas = ler.readlines()
		ler.close()

		self.puxar_da_nuvem = []
		if not os.listdir(pasta_faces):
			r = requests.post(server+'api/puxar_rosto', json={"ids":"TODOS"}, headers={"Authorization": "Bearer "+linhas[0]})
			if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
				if len(r.json()["result"]["dados"])> 0:
					nomes_json = os.path.join(self.appdata_path, "PontoLog\data.json")
					with open(nomes_json, "w") as arquivo:
						json.dump(r.json()["result"]["dados"], arquivo)

			else:
				tkmb.showerror(title="Error",message="foi possível se conectar com o servidor, Verifique a internet!")
		else:
			r = requests.post(server+'api/puxar_rosto', json={"ids":"TODOS"}, headers={"Authorization": "Bearer "+linhas[0]})
			if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
				if len(r.json()["result"]["dados"])> 0:
					nomes_json = os.path.join(self.appdata_path, "PontoLog\data.json")
					with open(nomes_json, "w") as arquivo:
						json.dump(r.json()["result"]["dados"], arquivo)
			else:
				tkmb.showerror(title="Error",message=" foi possível se conectar com o servidor, Verifique a internet!")
		with open(os.path.join(self.appdata_path, "PontoLog\data.json"), "r") as arquivo:
			ler = json.load(arquivo)
		for nome in ler:
			if(str(nome["id"])+"_"+ nome["user"]+".yml" in os.listdir(pasta_faces)) == False:
				self.linha = ctk.CTkFrame(self.ponto)
				self.linha.pack(padx=10, pady=10, fill=ctk.X)
				self.label = ctk.CTkLabel(master=self.linha,text=nome["user"].upper())
				self.label.pack(side=ctk.TOP, padx=10)

				self.button = ctk.CTkButton(master=self.linha,text='CADASTRAR ROSTO', command=lambda i=nome["id"], n=nome['user']: self.cadastro_rosto(i, n))
				self.button.pack(side=ctk.TOP)
			else:
				self.linha = ctk.CTkFrame(self.ponto)
				self.linha.pack(padx=10, pady=10, fill=ctk.X)
				self.label = ctk.CTkLabel(master=self.linha,text=nome["user"].upper())
				self.label.pack(side=ctk.TOP, padx=10)

				self.button = ctk.CTkButton(master=self.linha,text='BATER', command=lambda i=nome["id"] , n=nome['user']: self.bater(i, n))
				self.button.pack(side=ctk.TOP)
		self.variable_ready.set()
	def create_login(self):
		self.label = ctk.CTkLabel(master=self.login,text='Bater ponto')
		self.label.pack(pady=12,padx=10)


		self.user_entry= ctk.CTkEntry(master=self.login,placeholder_text="User")
		self.user_entry.pack(pady=12,padx=10)

		self.senha_entry= ctk.CTkEntry(master=self.login,placeholder_text="Senha", show="*")
		self.senha_entry.pack(pady=12,padx=10)


		self.button = ctk.CTkButton(master=self.login,text='CONFIRMAR',command=self.registrar)
		self.button.pack(pady=12,padx=10)
		self.variable_ready.set()
	def loading(self):
		self.label = ctk.CTkLabel(master=self.aguarde,text='AGUARDE...')
		self.label.pack(pady=12,padx=10)
	
	def registrar(self):
		self.current_frame.pack_forget()
		self.current_frame = self.aguarde
		self.current_frame.pack(fill='both',expand=True)

		file_path = os.path.join(self.appdata_path, "PontoLog\\log.txt")
		self.button.configure(state="disabled")

		if self.user_entry.get() != "":
			r = requests.post(server+'api/login_empresa', json={"user": (self.user_entry.get()).upper(), "senha": self.senha_entry.get()})
			if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
				f = open(file_path, "a")
				f.write(r.json()["result"]["token"])
				nomes_json = os.path.join(self.appdata_path, "PontoLog\data.json")

# Abrir o arquivo para escrita e gravar os dados JSON
				with open(nomes_json, "w") as arquivo:
					json.dump(r.json()["result"]["funcionarios"], arquivo)
				f.close()
				self.create_ponto()
				tkmb.showinfo(title="Login efetuado",message="Você conseguiu se logar!")
				self.current_frame.pack_forget()
				self.current_frame = self.ponto
				self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)
			else:
				tkmb.showerror(title="Error",message="VocêNão foi possível se conectar com o servidor, Verifique a internet!")
		else:
			tkmb.showerror(title="Error",message="Preencha o usuário e a senha")

	def bater(self, id, nome):
		file_path = os.path.join(self.appdata_path, "PontoLog\\log.txt")
		ler = open(file_path, "r")
		linhas = ler.readlines()
		ler.close()
		r = Reconhecimento( id, nome, self.appdata_path)
		if r == False:
			file_path = os.path.join(self.appdata_path, "PontoLog\\log.txt")
			ler = open(file_path, "r")
			linhas = ler.readlines()
			ler.close()
			r = requests.post(server+'api/ponto', json={"cod": id}, headers={"Authorization": "Bearer "+linhas[0]})

			if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
				if("cod_err" in r.json()["result"]):
					tkmb.showerror(title="Err",message="O código está errado")
				else:
					if( "ponto" in r.json()["result"]):
						if(r.json()["result"]["ponto"] == "saida"):
							tkmb.showinfo(title="Saida",message="Até Amanhâ")
						if(r.json()["result"]["ponto"] == "JA_SAIU"):
							tkmb.showerror(title="Erro",message="Você já saiu. Não pode mais bater ponto hoje")
					else:
						tkmb.showinfo(title="Ponto Batido",message="Bem-vindo")
			else:
				tkmb.showerror(title="Error",message="Não foi possivel bater seu ponto. Verifique sua internet e tente denovo")
	def show_frame(self):
		file_path = os.path.join(self.appdata_path, "PontoLog\\log.txt")
		f = os.path.join(self.appdata_path, "PontoLog\\data.json")
		if os.path.isfile(file_path) == True:
			ler = open(file_path, "r")
			linhas = ler.readlines()
			if len(linhas)> 0:
				log = ler.readlines()
				ler.close()
				self.create_ponto()

				self.current_frame = self.ponto
				self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)

			else:
				self.current_frame = self.login
				self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)

		else:
			l = open(f,"w")
			l.close()
			ler = open(file_path, "w")
			ler.close()
			self.current_frame = self.login
			self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)

	def cadastro_rosto(self, id, nome):
		CadastroRosto(str(id),nome)
		rosto_cod = Treinamento(id, nome)
		file_path = os.path.join(self.appdata_path, "PontoLog\\log.txt")
		data_json = os.path.join(self.appdata_path, "PontoLog\\data.json")
		ler = open(file_path, "r")
		linhas = ler.readlines()
		ler.close()
		r = requests.post(server+'api/upar_rosto', data={"face":rosto_cod, "id":id}, headers={"Authorization": "Bearer "+linhas[0]})
		if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
			with open(data_json, 'r') as file:
				dados = json.load(file)
			for linha in dados:
				if linha["id"] == id:
					linha["face"] = True
			with open(data_json, 'w') as file:
				json.dump(dados, file)
			for widget in self.ponto.winfo_children():
				widget.destroy()
			self.create_ponto()
			self.current_frame = self.ponto
			self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)
			tkmb.showinfo(title="Login efetuado",message="Rosto cadastrado!")
		else:
			tkmb.showerror(title="Error",message="Não foi possível se conectar com o servidor, Verifique a internet!")

class SplashScreen():
	def __init__(self, root):
		self.root = root
		self.root.geometry("400x400")
		self.root.title("PONTO ONLINE")
		self.frame = tk.Frame(self.root)
		self.label = tk.Label(self.frame, text="Aguarde até que a variável seja alterada.")
		self.label.pack(padx=20, pady=20)


def update_variable():
    global variable_ready
    variable_ready = True

def main():
	ctk.set_appearance_mode("dark")

	# Selecting color theme - blue, green, dark-blue
	ctk.set_default_color_theme("blue")
	tkmb.showinfo("Agurade", "Agurade enquanto fazemos as configurações e conectamos com o servidor.")
	nome_pasta = "PontoLog"
	dataset = "dataset"
	files_yml = "dataFace"
	variable_ready = False
	# Caminho completo para a pasta "AppData" do usuário (Unix-like)
	caminho_appdata = Path.home() / "AppData\Roaming"

	# Caminho completo da pasta que você deseja criar
	caminho_completo = caminho_appdata / nome_pasta

	# Criação da pasta
	if not caminho_completo.exists():
		caminho_completo.mkdir()
		(caminho_completo/dataset).mkdir()
		(caminho_completo/files_yml).mkdir()
	root = ctk.CTk()
	app = PontoOnline(root)
	app.variable_ready.wait()
	root.mainloop()
if __name__ == "__main__":
    main()
	
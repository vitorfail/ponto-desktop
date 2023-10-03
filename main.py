import customtkinter as ctk
import tkinter.messagebox as tkmb
import tkinter as tk
from tkinter import SUNKEN
import requests
import os
from api import server
import json
from cadastro_rosto import CadastroRosto 
from pathlib import Path
from treinamento import Treinamento
from reconhecimento import Reconhecimento
import threading
import time
from PIL import ImageTk, Image 

f = 0
nomes_json ={}
font_size= 12
font_style = "Arial"

def show_frame():
	path_app = os.getenv('APPDATA')
	file_path = os.path.join(path_app, "PontoLog\\log.txt")
	o = os.path.join(path_app, "PontoLog\\data.json")

	if os.path.isfile(file_path) == True:
		ler = open(file_path, "r")
		linhas = ler.readlines()
		if len(linhas)> 0:
			ler.close()
			r = requests.post(server+'api/puxar_rosto', json={"ids":"TODOS"}, headers={"Authorization": "Bearer "+linhas[0]})
			if(r.status_code == 200 and r.json()["result"]["status"] == "ok"):
				if len(r.json()["result"]["dados"])> 0:
					with open(o, "w") as arquivo:
						global nomes_json
						nomes_json = r.json()["result"]["dados"]
						json.dump(r.json()["result"]["dados"], arquivo)
			else:
				tkmb.showerror(title="Error",message="foi possível se conectar com o servidor, Verifique a internet!")
			global f 
			f =1
		else:
			f=0
			ler.close()
	else:
		l = open(o,"w")
		l.close()
		ler = open(file_path, "w")
		ler.close()

class PontoOnline():
	def __init__(self, root):
		self.variable_ready = threading.Event()
		self.appdata_path = os.getenv('APPDATA')
		self.texto_carregamento = "Aguarde estamos criando as pastas"
		self.root = root
		self.root.configure(bg='#1e1e1e')	
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

		if f == 1:
			self.create_ponto()
			self.current_frame = self.ponto
			self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)

		if f == 0:
			self.current_frame = self.login
			self.current_frame.pack(pady=20,padx=40,fill='both',expand=True)


		self.create_login()
        
	def create_ponto(self):
		pasta_faces = os.path.join(self.appdata_path, "PontoLog\dataFace")
		file_path = os.path.join(self.appdata_path, "PontoLog\log.txt")
		ler = open(file_path, "r")
		linhas = ler.readlines()
		ler.close()

		self.puxar_da_nuvem = []
		self.label2 = tk.Label(master=self.ponto,text='Lista de funcionários', bg="#272727", fg="white", font=(font_style, font_size))
		self.label2.pack(side=tk.TOP, padx=10)

		for nome in nomes_json:
			if(str(nome["id"])+"_"+ nome["user"]+".yml" in os.listdir(pasta_faces)) == False:
				self.linha = ctk.CTkFrame(self.ponto)
				self.linha.pack(padx=10, pady=10, fill=ctk.X)
				self.label = ctk.CTkLabel(master=self.linha,text=nome["user"].upper())
				self.label.pack(side=ctk.TOP, padx=10)

				self.button = ctk.CTkButton(master=self.linha,text='CADASTRAR ROSTO', command=lambda i=nome["id"], n=nome['user']: self.cadastro_rosto(i, n))
				self.button.pack(side=ctk.TOP)
				
			else:
				self.linha = ctk.CTkFrame(self.ponto)
				self.linha.pack(padx=10, pady=10, fill=tk.X)
				self.label = ctk.CTkLabel(master=self.linha,text=nome["user"].upper())
				self.label.pack(side=tk.TOP, padx=10)

				self.button = ctk.CTkButton(master=self.linha,text='BATER', command=lambda i=nome["id"] , n=nome['user']: self.bater(i, n))
				self.button.pack(side=ctk.TOP)				
				self.button.configure(bg='blue', fg='white')
		self.variable_ready.set()
	def create_login(self):
		self.label = ctk.CTkLabel(master=self.login,text='Bater ponto')		
		self.label.pack(pady=12,padx=10)

		self.user_entry= ctk.CTkEntry(master=self.login,placeholder_text="User")		
		self.user_entry.pack(pady=20,padx=20)

		self.senha_entry= ctk.CTkEntry(master=self.login,placeholder_text="Senha", show="*")
		self.senha_entry.pack(pady=20,padx=20)


		self.button = ctk.CTkButton(master=self.login,text='CONFIRMAR',command=self.registrar)
		self.button.pack(pady=12,padx=10)
		self.variable_ready.set()
		
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
				show_frame()
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
						if(r.json()["result"]["ponto"] == "JA_SAIU"):
							tkmb.showerror(title="Erro",message="Você já saiu. Não pode mais bater ponto hoje")
						else:
							tkmb.showinfo(title="Saida",message=r.json()["result"]["ponto"])

					else:
						tkmb.showinfo(title="Ponto Batido",message="Bem-vindo")
			else:
				tkmb.showerror(title="Error",message="Não foi possivel bater seu ponto. Verifique sua internet e tente denovo")
	def cadastro_rosto(self, id, nome):
		cad = CadastroRosto(str(id),nome)
		if cad == True:
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
		width_of_window = 427
		height_of_window = 250
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		x_coordinate = (screen_width/2)-(width_of_window/2)
		y_coordinate = (screen_height/2)-(height_of_window/2)
		self.root.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
		#w.configure(bg='#ED1B76')
		self.root.overrideredirect(1) #for hiding titlebar

		#new window to open

		self.frame = tk.Frame(self.root, width=427, height=250, bg='#272727').place(x=0,y=0)
		label1=tk.Label(self.root, text='PONTOONLINE', fg='white', bg='#272727') #decorate it 
		label1.configure(font=("Game Of Squids", 24, "bold"))   #You need to install this font in your PC or try another one
		label1.place(x=80,y=90)

		label2=tk.Label(self.root, text='Carregando...', fg='white', bg='#272727') #decorate it 
		label2.configure(font=("Calibri", 11))
		label2.place(x=10,y=215)

		#making animation

		image_a=ImageTk.PhotoImage(Image.open('c2.png'))
		image_b=ImageTk.PhotoImage(Image.open('c1.png'))

		for i in range(5): #5loops
			l1=tk.Label(self.root, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
			l2=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
			l3=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
			l4=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
			self.root.update_idletasks()
			time.sleep(0.2)

			l1=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
			l2=tk.Label(self.root, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
			l3=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
			l4=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
			self.root.update_idletasks()
			time.sleep(0.2)

			l1=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
			l2=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
			l3=tk.Label(self.root, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
			l4=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
			self.root.update_idletasks()
			time.sleep(0.2)

			l1=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
			l2=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
			l3=tk.Label(self.root, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
			l4=tk.Label(self.root, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
			self.root.update_idletasks()
			time.sleep(0.2)

def main():
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("blue")

	splash = tk.Tk()
	app1 = SplashScreen(splash)
	splash.destroy()
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
	show_frame()		
	root = ctk.CTk()	
	app = PontoOnline(root)
	root.mainloop()
	splash.mainloop()


if __name__ == "__main__":
    main()
	
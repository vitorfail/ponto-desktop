import tkinter as tk
from tkinter import ttk

# Crie uma instância da janela principal
janela = tk.Tk()
janela.title("Frame com Barra de Rolagem")

# Crie um widget Canvas
canvas = tk.Canvas(janela)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crie um widget Scrollbar
scrollbar = ttk.Scrollbar(janela, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure a barra de rolagem para rolar o canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Crie um widget Frame dentro do Canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Adicione alguns widgets ao Frame (apenas como exemplo)
for i in range(30):
    label = tk.Label(frame, text=f"Item {i}")
    label.pack()

# Configurar o evento para ajustar o tamanho do canvas quando o conteúdo do frame mudar
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Inicialize a janela
janela.mainloop()

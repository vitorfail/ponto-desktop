import tkinter as tk
import time

root = tk.Tk()
root.title("Janela Principal")
frame = tk.Frame(root)
label = tk.Label(master=frame,text='Bater ponto')
label.pack(pady=12,padx=10)


# Oculta a janela principal

time.sleep(3)
# Cria uma nova janela
new_window = tk.Toplevel(root)
new_window.title("Nova Janela")

label = tk.Label(new_window, text="Esta é uma nova janela.")
label.pack(pady=20)

root.mainloop()
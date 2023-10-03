from tkinter import *
 
# Create Tk object
window = Tk()
 
# Set the window title
window.title('GFG')
 
# Entry Widget
# highlightthickness for thickness of the border
entry = Entry(highlightthickness=2)
 
# highlightbackground and highlightcolor for the border color
entry.config(highlightbackground = "red", highlightcolor= "red")
 
# Place the widgets in window
entry.pack(padx=20, pady=20)
 
window.mainloop()
import tkinter as tk
import os
window = tk.Tk()
geo = window.geometry
geo("800x800+800+800")
window.title("Button GUI")

# get the list of files
currentDir = os.getcwd()
flist = os.listdir(currentDir + '/20 Minutos/Salud')
 
lbox = tk.Listbox(window)
label20Min = tk.Label(window, text="20 Minutos")
label20Min.grid(row=1, column=0)
lbox.grid(row=2, column=0)
 
# THE ITEMS INSERTED WITH A LOOP
for item in flist:
    lbox.insert(tk.END, item)

tk.mainloop()
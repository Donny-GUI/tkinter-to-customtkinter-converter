import tkinter as tk 
import customtkinter as ctk


root = tk.Tk()
scale = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
cscale = ctk.CTkSlider(root, from_=0, to=1, resolution=0.01, orientation=tk.HORIZONTAL)
root.mainloop()


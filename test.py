import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Listbox Example")

# Create a tkinter Listbox
tk_listbox = tk.Listbox(root)
tk_listbox.pack(side=tk.LEFT, padx=10, pady=10)

# Insert items into the tkinter Listbox
for i in range(10):
    tk_listbox.insert(tk.END, f"Item {i+1}")

# Create a ttk Listbox
ttk_listbox = ttk.Listbox(root)
ttk_listbox.pack(side=tk.RIGHT, padx=10, pady=10)

# Insert items into the ttk Listbox
for i in range(10):
    ttk_listbox.insert(tk.END, f"Item {i+1}")

# Run the Tkinter event loop
root.mainloop()

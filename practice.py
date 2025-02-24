import ast 

x = ast.parse("entry_name = ctk.CTkEntry(root, font=('Arial', 12), fg_color='black', bg_color='white', width=25, bd=3, relief=tk.GROOVE, justify='left')")

y = ast.dump(x, annotate_fields=True, indent=4)

print(y)
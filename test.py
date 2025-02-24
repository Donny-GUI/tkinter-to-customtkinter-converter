import tkinter as tk

def submit():
    label_result.config(text=f"Name: {entry_name.get()}\nPassword: {entry_password.get()}\nGender: {var_gender.get()}")

# Create main window
root = tk.Tk()
root.title("Tkinter Widgets with Keyword Arguments Demo")
root.geometry("600x400")
root.config(bg="lightgray")

# Label widget with all possible kwargs
label = tk.Label(root, text="This is a label widget", font=("Arial", 12), fg="blue", bg="lightyellow", relief=tk.SOLID, padx=10, pady=10, width=20, height=2, anchor="center")
label.pack(pady=10)

# Button widget with all possible kwargs
button = tk.Button(root, text="Submit", command=submit, font=("Arial", 12), fg="white", bg="green", relief=tk.RAISED, width=20, height=2, bd=5, activebackground="lightgreen", activeforeground="blue")
button.pack(pady=10)

# Entry widget with all possible kwargs
label_name = tk.Label(root, text="Name:")
label_name.pack(pady=5)
entry_name = tk.Entry(root, font=("Arial", 12), fg="black", bg="white", width=25, bd=3, relief=tk.GROOVE, justify="left")
entry_name.pack(pady=5)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*", font=("Arial", 12), fg="black", bg="white", width=25, bd=3, relief=tk.GROOVE, justify="left")
entry_password.pack(pady=5)

# Checkbutton widget with all possible kwargs
checkbutton = tk.Checkbutton(root, text="Remember me", font=("Arial", 12), fg="black", bg="lightblue", anchor="w", justify="left", variable=tk.BooleanVar())
checkbutton.pack(pady=10)

# Radiobutton widget with all possible kwargs
var_gender = tk.StringVar()
radiobutton_male = tk.Radiobutton(root, text="Male", variable=var_gender, value="Male", font=("Arial", 12), fg="black", bg="lightblue", anchor="w", justify="left", width=20)
radiobutton_female = tk.Radiobutton(root, text="Female", variable=var_gender, value="Female", font=("Arial", 12), fg="black", bg="lightblue", anchor="w", justify="left", width=20)
radiobutton_male.pack()
radiobutton_female.pack()

# Scale widget with all possible kwargs
label_scale = tk.Label(root, text="Select a value:")
label_scale.pack(pady=5)
scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, font=("Arial", 12), length=300, tickinterval=20, sliderlength=20, showvalue=True, bd=2, relief=tk.SUNKEN)
scale.pack(pady=5)

# Listbox widget with all possible kwargs
listbox = tk.Listbox(root, height=5, width=30, font=("Arial", 12), bg="lightyellow", selectmode=tk.SINGLE, bd=2, relief=tk.GROOVE, exportselection=False)
for item in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert(tk.END, item)
listbox.pack(pady=10)

# OptionMenu widget with all possible kwargs
label_combobox = tk.Label(root, text="Select an option:")
label_combobox.pack(pady=5)
combobox = tk.OptionMenu(root, tk.StringVar(), "Option 1", "Option 2", "Option 3", font=("Arial", 12), width=20, bg="lightgreen", fg="black", relief=tk.GROOVE)
combobox.pack(pady=5)

# Text widget with all possible kwargs
text_widget = tk.Text(root, height=5, width=40, font=("Arial", 12), bg="lightblue", fg="black", wrap=tk.WORD, padx=10, pady=10, bd=3, relief=tk.RAISED)
text_widget.insert(tk.END, "This is a text widget\n")
text_widget.pack(pady=10)

# Canvas widget with all possible kwargs
canvas = tk.Canvas(root, width=200, height=100, bg="lightblue", bd=5, relief=tk.RAISED)
canvas.create_rectangle(50, 25, 150, 75, fill="yellow")
canvas.create_oval(50, 25, 150, 75, fill="green")
canvas.pack(pady=10)

# Menu widget with all possible kwargs
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0, bg="lightgray", fg="black")
file_menu.add_command(label="Open", font=("Arial", 12), command=lambda: print("Open clicked"))
file_menu.add_command(label="Save", font=("Arial", 12), command=lambda: print("Save clicked"))
file_menu.add_separator()
file_menu.add_command(label="Exit", font=("Arial", 12), command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

# Scrollbar widget with all possible kwargs
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# LabelFrame widget with all possible kwargs
labelframe = tk.LabelFrame(root, text="Label Frame", padx=10, pady=10, font=("Arial", 12), bg="lightyellow", fg="black", bd=3, relief=tk.SUNKEN)
labelframe.pack(padx=10, pady=10, fill="both", expand=True)
label_in_labelframe = tk.Label(labelframe, text="This is inside a LabelFrame", font=("Arial", 12), fg="black")
label_in_labelframe.pack(pady=5)

# PanedWindow widget with all possible kwargs
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.SUNKEN, bg="lightgray")
frame_left = tk.Frame(paned_window, width=100, height=100, bg="lightgrey")
frame_right = tk.Frame(paned_window, width=100, height=100, bg="lightgreen")
paned_window.add(frame_left)
paned_window.add(frame_right)
paned_window.pack(pady=10, fill="both", expand=True)

# Frame widget with all possible kwargs
frame = tk.Frame(root, borderwidth=5, relief=tk.SUNKEN, bg="lightgreen", padx=10, pady=10)
frame.pack(padx=10, pady=10)
frame_label = tk.Label(frame, text="This is a frame", font=("Arial", 12), fg="black")
frame_label.pack(pady=5)

# Message widget with all possible kwargs
message = tk.Message(root, text="This is a message widget", width=200, font=("Arial", 12), bg="lightyellow", fg="black", anchor="center")
message.pack(pady=10)

# After all the widgets and variables, display the result
label_result = tk.Label(root, text="Results will be shown here.", font=("Arial", 12), fg="black", bg="lightblue")
label_result.pack(pady=20)

# Start the main event loop
root.mainloop()

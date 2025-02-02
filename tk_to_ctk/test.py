import tkinter as tk
from tkinter import filedialog
import subprocess



def search_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, content)

def convert_file():
    file_content = text_box.get(1.0, tk.END)
    # Perform file conversion here
    # For example, let's just print the content for demonstration
    print("Converted file content:")
    print(file_content)

# Create the main window
root = tk.Tk()
root.title("Python File Converter")

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create a Search button
search_button = tk.Button(button_frame, text="Search File", command=search_file)
search_button.pack(side=tk.LEFT, padx=5)

# Create a Convert button
convert_button = tk.Button(button_frame, text="Convert File", command=convert_file)
convert_button.pack(side=tk.LEFT, padx=5)

# Create a text box to display file content
text_box = tk.Text(root, wrap="word", width=50, height=20)
text_box.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
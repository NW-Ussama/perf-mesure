import tkinter as tk

# Function to print the input content
def print_input():
    input_content = input_entry.get()
    print("Input:", input_content)

# UI Setup
root = tk.Tk()
root.title("Minimal Example")

# Create and pack the input field with visible foreground and background colors
input_entry = tk.Entry(root, width=50, bg='white', fg='black', highlightbackground='black', highlightcolor='black')
input_entry.pack(padx=10, pady=10)

# Create and pack the button
submit_button = tk.Button(root, text="Print Input", command=print_input)
submit_button.pack(padx=10, pady=10)

# Run the GUI
root.mainloop()

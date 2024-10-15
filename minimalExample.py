import tkinter as tk

# Function to handle button click
def on_button_click():
    # Get the content of the text input
    input_text = text_entry.get()
    print(input_text)

# UI Setup
root = tk.Tk()
root.title("Minimal Tkinter Example")

# Set window geometry
root.geometry("300x150")

# Create a label
label = tk.Label(root, text="Enter something:")
label.grid(row=0, column=0, padx=10, pady=5)

# Create a text input
text_entry = tk.Entry(root, width=30)
text_entry.grid(row=1, column=0, padx=10, pady=5)

# Create a button
button = tk.Button(root, text="Print Input", command=on_button_click)
button.grid(row=2, column=0, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()

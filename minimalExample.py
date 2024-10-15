import tkinter as tk
from tkinter import ttk

# Function to print the input content
def print_input():
    input_content = input_entry.get()
    print("Input:", input_content)

# UI Setup
root = tk.Tk()
root.title("Minimal Example")

# Set the background color of the root window
root.configure(bg='lightgray')

# Create a frame to hold the input and button
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create and pack the input field with ttk
input_entry = ttk.Entry(frame, width=50)
input_entry.pack(pady=5)

# Create and pack the button
submit_button = ttk.Button(frame, text="Print Input", command=print_input)
submit_button.pack(pady=5)

# Run the GUI
root.mainloop()

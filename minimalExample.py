import tkinter as tk

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
frame = tk.Frame(root, bg='lightgray')
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create and pack the input field
input_entry = tk.Entry(frame, width=50, bg='white', fg='black')
input_entry.pack(pady=5)

# Create and pack the button
submit_button = tk.Button(frame, text="Print Input", command=print_input, bg='blue', fg='white')
submit_button.pack(pady=5)

# Run the GUI
root.mainloop()

import tkinter as tk

print("tkinter.TkVersion :: ", tk.TkVersion)

# Function to handle button click
def on_button_click():
    input_text = text_entry.get()
    print(input_text)

# UI Setup
root = tk.Tk()
root.title("Tkinter Debug Example")

# Set window geometry
root.geometry("300x150")

# Create a frame for better organization
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a label
label = tk.Label(frame, text="Enter something:")
label.pack(pady=5)

# Create a text input
text_entry = tk.Entry(frame, width=30)
text_entry.pack(pady=5)

# Create a button
button = tk.Button(frame, text="Print Input", command=on_button_click)
button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

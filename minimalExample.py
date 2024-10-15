import tkinter as tk

def perform_requests():
    print("Button clicked!")

root = tk.Tk()
root.title("Test Layout")

# Basic layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

url_label = tk.Label(frame, text="Link:")
url_label.grid(row=0, column=0, sticky='e')
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1)

submit_button = tk.Button(frame, text="Perform Requests", command=perform_requests)
submit_button.grid(row=1, columnspan=2)

root.mainloop()

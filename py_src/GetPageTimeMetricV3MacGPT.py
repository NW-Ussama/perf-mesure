import tkinter as tk
from tkinter import messagebox
import requests
import time
import statistics
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Use TkAgg backend for macOS compatibility
matplotlib.use('TkAgg')

# Function to perform requests and display results
def perform_requests():
    url = url_entry.get()
    cookie = cookie_entry.get()
    try:
        repeat = int(repeat_entry.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid integer for Repeat")
        return

    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL")
        return

    try:
        headers = {'Cookie': cookie} if cookie else {}
        durations = []

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        ax_hist.cla()
        ax_line.cla()

        for i in range(repeat):
            start_time = time.time()
            response = requests.get(url, headers=headers)
            end_time = time.time()
            duration = end_time - start_time
            durations.append(duration)

            duration_range = math.ceil(max(durations)) - math.floor(min(durations)) if len(durations) > 1 else 0.5
            num_bins = max(1, int(duration_range / 0.5))

            ax_hist.cla()
            ax_hist.hist(durations, bins=num_bins, edgecolor='black', alpha=0.7)
            ax_hist.set_title(f"Frequency of Request Durations ({i+1}/{repeat} Requests)")
            ax_hist.set_xlabel("Duration (seconds)")
            ax_hist.set_ylabel("Number of Requests")
            canvas_hist.draw()

            ax_line.cla()
            ax_line.plot(durations, marker='o', linestyle='-', color='blue')
            ax_line.set_title(f"Duration per Request ({i+1}/{repeat} Requests)")
            ax_line.set_xlabel("Request Index")
            ax_line.set_ylabel("Duration (seconds)")
            canvas_line.draw()

            root.update_idletasks()

        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        min_duration = min(durations)
        stddev_duration = statistics.stdev(durations) if len(durations) > 1 else 0

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Average Duration: {avg_duration:.4f} seconds\n")
        result_text.insert(tk.END, f"Maximum Duration: {max_duration:.4f} seconds\n")
        result_text.insert(tk.END, f"Minimum Duration: {min_duration:.4f} seconds\n")
        result_text.insert(tk.END, f"Standard Deviation: {stddev_duration:.4f} seconds\n")
        result_text.config(state=tk.DISABLED)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"An error occurred: {e}")

# UI Setup
root = tk.Tk()
root.title("GET Request Duration Checker")

# Set the window geometry and make it resizable
root.geometry("1000x600")
root.grid_rowconfigure(0, weight=1)  # Make rows and columns stretchable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Input fields and result text frame
input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Ensure the input fields and result text frame expand
url_label = tk.Label(input_frame, text="Link:")
url_label.grid(row=0, column=0, sticky='e', pady=5)
url_entry = tk.Entry(input_frame, width=50)
url_entry.grid(row=0, column=1, pady=5)

cookie_label = tk.Label(input_frame, text="Cookie:")
cookie_label.grid(row=1, column=0, sticky='e', pady=5)
cookie_entry = tk.Entry(input_frame, width=50)
cookie_entry.grid(row=1, column=1, pady=5)

repeat_label = tk.Label(input_frame, text="Repeat:")
repeat_label.grid(row=2, column=0, sticky='e', pady=5)
repeat_entry = tk.Entry(input_frame, width=50)
repeat_entry.grid(row=2, column=1, pady=5)

submit_button = tk.Button(input_frame, text="Perform Requests", command=perform_requests)
submit_button.grid(row=3, columnspan=2, pady=10)

# Result text area
result_frame = tk.Frame(input_frame)
result_frame.grid(row=4, column=0, columnspan=2, pady=10)

result_text = tk.Text(result_frame, height=6, width=50, state=tk.DISABLED)
result_text.pack(fill=tk.BOTH, expand=True)

# Histogram and line chart frames
hist_frame = tk.Frame(main_frame)
hist_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
main_frame.grid_columnconfigure(1, weight=1)

fig_hist, ax_hist = plt.subplots()
canvas_hist = FigureCanvasTkAgg(fig_hist, master=hist_frame)
canvas_hist.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

line_frame = tk.Frame(main_frame)
line_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
main_frame.grid_columnconfigure(2, weight=1)

fig_line, ax_line = plt.subplots()
canvas_line = FigureCanvasTkAgg(fig_line, master=line_frame)
canvas_line.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()

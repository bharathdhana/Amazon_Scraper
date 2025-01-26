import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import pandas as pd
import json
import csv

# Import your scraping functions
from scrap import scrape_amazon  # Replace with the actual filename

# Function to start the scraping process
def start_scraping():
    keyword = keyword_entry.get().strip()
    file_format = file_format_var.get()

    if not keyword:
        messagebox.showerror("Error", "Please enter a product keyword!")
        return

    if not file_format:
        messagebox.showerror("Error", "Please select a file format!")
        return

    def scrape_and_save():
        try:
            progress_label.config(text="Scraping data... Please wait.")
            data = scrape_amazon(keyword)

            if data:
                save_data_to_file(data, file_format)
                progress_label.config(text="Scraping and saving completed!")
            else:
                progress_label.config(text="No data found for the given keyword.")
        except Exception as e:
            progress_label.config(text="An error occurred during scraping.")
            messagebox.showerror("Error", str(e))

    Thread(target=scrape_and_save, daemon=True).start()

# Function to save data to file
def save_data_to_file(data, file_format):
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_format}",
                                             filetypes=[(f"{file_format.upper()} files", f"*.{file_format}")])
    if not file_path:
        return

    try:
        if file_format == "csv":
            keys = data[0].keys()
            with open(file_path, "w", newline="", encoding="utf-8") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
        elif file_format == "json":
            with open(file_path, "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)
        elif file_format == "excel":
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
        else:
            messagebox.showerror("Error", "Unsupported file format. Please choose csv, json, or excel.")
            return

        messagebox.showinfo("Success", f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

# Create the main application window
app = tk.Tk()
app.title("Amazon Scraper")
app.geometry("400x300")

# Keyword input
tk.Label(app, text="Enter Product Keyword:").pack(pady=5)
keyword_entry = tk.Entry(app, width=40)
keyword_entry.pack(pady=5)

# File format selection
tk.Label(app, text="Select File Format:").pack(pady=5)
file_format_var = tk.StringVar()
file_format_combobox = ttk.Combobox(app, textvariable=file_format_var, state="readonly")
file_format_combobox["values"] = ("csv", "json", "excel")
file_format_combobox.pack(pady=5)

# Start scraping button
scrape_button = tk.Button(app, text="Start Scraping", command=start_scraping)
scrape_button.pack(pady=20)

# Progress label
progress_label = tk.Label(app, text="", fg="green")
progress_label.pack(pady=10)

# Run the application
app.mainloop()
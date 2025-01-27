import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_comments_and_logs(file_content, file_type):
    """
    Removes comments, console.logs (except console.error and alert()) from the content
    based on file type.
    """
    if file_type == "js":
        # Remove console.logs (except console.error and alert)
        file_content = re.sub(r'console\.log\(.*?\);?\s*', '', file_content)
        # Remove single-line comments
        file_content = re.sub(r'//.*', '', file_content)
        # Remove multi-line comments
        file_content = re.sub(r'/\*.*?\*/', '', file_content, flags=re.DOTALL)
    elif file_type in ["html", "css"]:
        # Remove HTML and CSS comments
        file_content = re.sub(r'/\*.*?\*/', '', file_content, flags=re.DOTALL)
        file_content = re.sub(r'<!--.*?-->', '', file_content, flags=re.DOTALL)
    return file_content

def process_files(input_folder, output_folder):
    """
    Processes files from input_folder and saves cleaned files to output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input_folder)
            output_file_path = os.path.join(output_folder, relative_path)

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            file_extension = file.split(".")[-1].lower()
            if file_extension in ["html", "js", "css"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                cleaned_content = remove_comments_and_logs(content, file_extension)
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_content)
            else:
                # Copy other files as-is
                shutil.copy2(file_path, output_file_path)

def browse_folder():
    """Opens a dialog to select a folder."""
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def clean_project():
    """Cleans the project by removing comments and logs."""
    folder_path = folder_entry.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid Firebase project folder.")
        return

    public_folder = os.path.join(folder_path, "public")
    if not os.path.exists(public_folder):
        messagebox.showerror("Error", "The selected folder does not contain a 'public' directory.")
        return

    output_folder = os.path.join(folder_path, "cleaned")
    process_files(public_folder, output_folder)
    messagebox.showinfo("Success", f"Cleaned project has been saved to: {output_folder}")

# Create GUI
root = tk.Tk()
root.title("Firebase Project Cleaner")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

folder_label = tk.Label(frame, text="Select Firebase Project Folder:")
folder_label.grid(row=0, column=0, sticky="w")

folder_entry = tk.Entry(frame, width=50)
folder_entry.grid(row=1, column=0, padx=5, pady=5)

browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=1, padx=5, pady=5)

clean_button = tk.Button(frame, text="Clean Project", command=clean_project)
clean_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

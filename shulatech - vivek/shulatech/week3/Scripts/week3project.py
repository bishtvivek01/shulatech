import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File categories based on extensions
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css']
}

def organize_files(directory):
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Selected directory does not exist!")
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            
            for category, extensions in FILE_CATEGORIES.items():
                if file_ext in extensions:
                    category_path = os.path.join(directory, category)
                    if not os.path.exists(category_path):
                        os.makedirs(category_path)
                    shutil.move(file_path, os.path.join(category_path, filename))
                    break  # Stop checking once a category is found
    
    messagebox.showinfo("Success", "Files organized successfully!")

def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organize_files(folder_selected)

# GUI setup
root = tk.Tk()
root.title("File Organizer")
root.geometry("300x200")

title_label = tk.Label(root, text="Select a folder to organize", font=("Arial", 12))
title_label.pack(pady=20)

select_button = tk.Button(root, text="Select Folder", command=select_directory, font=("Arial", 10))
select_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=10)

root.mainloop()

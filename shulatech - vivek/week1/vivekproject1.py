# import tkinter as tk
# from tkinter import messagebox
# import sqlite3

# # Database setup
# conn = sqlite3.connect("todo.db")
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
# conn.commit()

# def add_task():
#     task = task_entry.get()
#     if task:
#         cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
#         conn.commit()
#         task_list.insert(tk.END, task)
#         task_entry.delete(0, tk.END)

# def delete_task():
#     try:
#         selected_task = task_list.curselection()[0]
#         task_text = task_list.get(selected_task)
#         cursor.execute("DELETE FROM tasks WHERE task=?", (task_text,))
#         conn.commit()
#         task_list.delete(selected_task)
#     except IndexError:
#         messagebox.showwarning("Warning", "Please select a task to delete.")

# def load_tasks():
#     cursor.execute("SELECT task FROM tasks")
#     tasks = cursor.fetchall()
#     for task in tasks:
#         task_list.insert(tk.END, task[0])

# # GUI setup
# root = tk.Tk()
# root.title("To-Do List")

# task_entry = tk.Entry(root, width=40)
# task_entry.pack(pady=10)

# add_button = tk.Button(root, text="Add Task", command=add_task)
# add_button.pack()

# delete_button = tk.Button(root, text="Delete Task", command=delete_task)
# delete_button.pack()

# task_list = tk.Listbox(root, width=50)
# task_list.pack(pady=10)

# load_tasks()
# root.mainloop()

# conn.close()


import sqlite3
import tkinter as tk
from tkinter import messagebox
import smtplib
import os
from datetime import datetime
from email.message import EmailMessage

# Get absolute path of the database file
DB_PATH = os.path.abspath("todo.db")

# Database connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY, 
        task TEXT NOT NULL, 
        due_date TEXT NOT NULL
    )
""")
conn.commit()

# Function to add a task
def add_task():
    task = task_entry.get().strip()
    due_date = due_date_entry.get().strip()

    if task and due_date:
        try:
            cursor.execute("INSERT INTO tasks (task, due_date) VALUES (?, ?)", (task, due_date))
            conn.commit()
            list_tasks()
            task_entry.delete(0, tk.END)
            due_date_entry.delete(0, tk.END)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding task: {e}")
    else:
        messagebox.showwarning("Warning", "Task and Due Date cannot be empty")

# Function to list tasks
def list_tasks():
    task_list.delete(0, tk.END)
    
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    
    if not rows:
        task_list.insert(tk.END, "No tasks found")
    else:
        for row in rows:
            if len(row) < 3:  # Ensure proper data structure
                continue
            task_list.insert(tk.END, f"{row[1]} (Due: {row[2]})")  # row[1] = task, row[2] = due_date

# Function to delete a task
def delete_task():
    selected_task = task_list.get(tk.ACTIVE)
    if not selected_task or selected_task == "No tasks found":
        messagebox.showwarning("Warning", "No task selected to delete")
        return

    task_name = selected_task.split(" (Due:")[0]
    try:
        cursor.execute("DELETE FROM tasks WHERE task=?", (task_name,))
        conn.commit()
        list_tasks()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error deleting task: {e}")

# Function to send email reminders
def send_reminders():
    EMAIL = os.getenv("EMAIL_USER", "email@gmail.com")  
    PASSWORD = os.getenv("EMAIL_PASS", "email_password")  

    cursor.execute("SELECT task FROM tasks WHERE due_date=?", (datetime.today().strftime('%Y-%m-%d'),))
    tasks_due_today = cursor.fetchall()

    if not tasks_due_today:
        messagebox.showinfo("No Reminders", "No tasks due today.")
        return

    message_content = "\n".join(task[0] for task in tasks_due_today)

    msg = EmailMessage()
    msg.set_content(f"Tasks due today:\n\n{message_content}")
    msg["Subject"] = "To-Do List Reminder"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        messagebox.showinfo("Reminder Sent", "Email reminder sent successfully!")
    except Exception as e:
        messagebox.showerror("Email Error", f"Error sending email: {e}")

# GUI setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

tk.Label(root, text="Task:").pack()
task_entry = tk.Entry(root, width=40)
task_entry.pack()

tk.Label(root, text="Due Date (YYYY-MM-DD):").pack()
due_date_entry = tk.Entry(root, width=40)
due_date_entry.pack()

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

reminder_button = tk.Button(root, text="Send Reminders", command=send_reminders)
reminder_button.pack()

task_list = tk.Listbox(root, width=50, height=10)
task_list.pack()

# Show database location
tk.Label(root, text=f"Database: {DB_PATH}", fg="blue").pack()

list_tasks()
root.mainloop()


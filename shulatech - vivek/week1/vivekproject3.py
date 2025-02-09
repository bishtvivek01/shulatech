import tkinter as tk
import random
import string

def generate_password():
    length = int(length_entry.get())
    characters = string.ascii_letters + string.digits
    if special_var.get():
        characters += string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    password_var.set(password)

def save_password():
    password = password_var.get()
    if password:
        with open("passwords.txt", "a") as file:
            file.write(password + "\n")

# GUI setup
root = tk.Tk()
root.title("Password Generator")

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

special_var = tk.BooleanVar()
tk.Checkbutton(root, text="Include Special Characters", variable=special_var).pack()

tk.Button(root, text="Generate Password", command=generate_password).pack()

password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, width=30).pack()

tk.Button(root, text="Save Password", command=save_password).pack()

root.mainloop()

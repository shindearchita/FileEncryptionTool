import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import base64
import hashlib
import os

# -------- Key Generator --------
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# -------- Encrypt Function --------
def encrypt_file(filename, password):
    if not os.path.exists(filename):
        messagebox.showerror("Error", "File not found!")
        return

    key = generate_key(password)
    f = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    output_name = filename + ".enc"
    with open(output_name, "wb") as file:
        file.write(encrypted)

    messagebox.showinfo("Success", f"✅ File Encrypted!\nSaved As: {output_name}")

# -------- Decrypt Function --------
def decrypt_file(filename, password):
    if not os.path.exists(filename):
        messagebox.showerror("Error", "File not found!")
        return

    key = generate_key(password)
    f = Fernet(key)

    try:
        with open(filename, "rb") as file:
            data = file.read()

        decrypted = f.decrypt(data)

        output_name = "decrypted_" + filename.replace(".enc", "")
        with open(output_name, "wb") as file:
            file.write(decrypted)

        # Auto-open file on Windows
        full_path = os.path.abspath(output_name)
        if os.name == 'nt':
            os.startfile(full_path)

        messagebox.showinfo("Success", f"✅ File Decrypted!\nSaved As: {output_name}")

    except:
        messagebox.showerror("Error", "❌ Incorrect Password or File Corrupted!")

# -------- GUI --------
root = tk.Tk()
root.title("File Encryption Tool")
root.geometry("450x300")

selected_file = ""

def browse_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_label.config(text=selected_file)

def encrypt_gui():
    if not selected_file:
        messagebox.showerror("Error", "No file selected!")
        return
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Enter a password!")
        return
    encrypt_file(selected_file, password)

def decrypt_gui():
    if not selected_file:
        messagebox.showerror("Error", "No file selected!")
        return
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Enter a password!")
        return
    decrypt_file(selected_file, password)

# UI Elements
file_label = tk.Label(root, text="No file selected", wraplength=400)
file_label.pack(pady=10)

browse_btn = tk.Button(root, text="Select File", width=30, command=browse_file)
browse_btn.pack(pady=5)

password_label = tk.Label(root, text="Enter Password:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, show="*", width=35)
password_entry.pack(pady=5)

encrypt_btn = tk.Button(root, text="Encrypt File", width=30, command=encrypt_gui)
encrypt_btn.pack(pady=10)

decrypt_btn = tk.Button(root, text="Decrypt File", width=30, command=decrypt_gui)
decrypt_btn.pack(pady=5)

root.mainloop()

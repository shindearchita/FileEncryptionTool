import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import base64
import hashlib
import os
import logging
import re
from datetime import datetime

# -------- Key Generator --------
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# -------- Activity Logger --------
def write_log(action, filename):
    with open("activity.log", "a") as log:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{time} - {action} - {os.path.basename(filename)}\n")

# -------- Encrypt Function --------
def encrypt_file(filename, password):

    if not os.path.exists(filename):
        messagebox.showerror("Error", "File not found!")
        return

    # -------- File Validation --------

    file_size = os.path.getsize(filename)

    if file_size == 0:
        messagebox.showerror(
            "Error",
            "The selected file is empty."
        )
        return

    if file_size > 100 * 1024 * 1024:
        proceed = messagebox.askyesno(
            "Large File",
            "This file is larger than 100 MB.\n\nDo you want to continue?"
        )

        if not proceed:
            return

    key = generate_key(password)
    f = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    output_name = filename + ".enc"

    with open(output_name, "wb") as file:
        file.write(encrypted)

    write_log("ENCRYPT", filename)

    messagebox.showinfo(
        "Success",
        f"✅ File Encrypted!\nSaved As: {output_name}"
    )

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

        output_name = "decrypted_" + os.path.basename(filename.replace(".enc", ""))

        with open(output_name, "wb") as file:
            file.write(decrypted)

        # Auto-open file on Windows
        full_path = os.path.abspath(output_name)

        if os.name == 'nt':
            os.startfile(full_path)

        write_log("DECRYPT", filename)

        messagebox.showinfo(
            "Success",
            f"✅ File Decrypted!\nSaved As: {output_name}"
        )

    except Exception as e:
        print("Decrypt Error:", e)

    write_log("FAILED DECRYPT ATTEMPT", filename)

    messagebox.showerror(
        "Error",
        f"Error: {e}"
    )


def check_password_strength(event=None):

    password = password_entry.get()

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        strength_label.config(
            text="Strength: 🔴 Weak",
            fg="red"
        )

    elif score == 3 or score == 4:
        strength_label.config(
            text="Strength: 🟡 Medium",
            fg="orange"
        )

    else:
        strength_label.config(
            text="Strength: 🟢 Strong",
            fg="green"
        )

# -------- GUI --------
root = tk.Tk()
root.title("🔐 File Encryption Tool v2.0")
root.geometry("600x420")
root.resizable(False, False)
root.configure(bg="#f5f7fa")

selected_file = ""

# ---------------- Functions ----------------

def browse_file():
    global selected_file
    selected_file = filedialog.askopenfilename()

    if selected_file:
        file_label.config(text=f"📄 {os.path.basename(selected_file)}")
        status_label.config(text="Status: File Selected ✅")
    else:
        file_label.config(text="No file selected")
        status_label.config(text="Status: Ready")


def encrypt_gui():
    if not selected_file:
        messagebox.showerror("Error", "Please select a file first.")
        return

    password = password_entry.get()

    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    encrypt_file(selected_file, password)
    status_label.config(text="Status: Encryption Successful ✅")


def decrypt_gui():
    if not selected_file:
        messagebox.showerror("Error", "Please select a file first.")
        return

    password = password_entry.get()

    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    decrypt_file(selected_file, password)
    status_label.config(text="Status: Decryption Successful ✅")


# ---------------- Title ----------------

title_label = tk.Label(
    root,
    text="🔐 File Encryption Tool",
    font=("Segoe UI", 18, "bold"),
    bg="#f5f7fa",
    fg="#1f3c88"
)
title_label.pack(pady=15)

# ---------------- File ----------------

tk.Label(
    root,
    text="Selected File",
    font=("Segoe UI", 11, "bold"),
    bg="#f5f7fa"
).pack()

file_label = tk.Label(
    root,
    text="No file selected",
    bg="white",
    width=55,
    relief="solid",
    anchor="w"
)
file_label.pack(pady=5)

browse_btn = tk.Button(
    root,
    text="📂 Browse File",
    command=browse_file,
    bg="#4CAF50",
    fg="white",
    width=20
)
browse_btn.pack(pady=10)

# ---------------- Password ----------------

tk.Label(
    root,
    text="Password",
    font=("Segoe UI", 11, "bold"),
    bg="#f5f7fa"
).pack()

password_entry = tk.Entry(root, show="*", width=35)
password_entry.pack(pady=5)

password_entry.bind("<KeyRelease>", check_password_strength)

# Show/Hide Password
def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

show_password_var = tk.BooleanVar()

show_password = tk.Checkbutton(
    root,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password,
    bg="#f5f7fa"
)

show_password.pack()

strength_label = tk.Label(
    root,
    text="Strength: ",
    font=("Segoe UI", 10, "bold"),
    bg="#f5f7fa"
)

strength_label.pack(pady=5)

# ---------------- Buttons ----------------

button_frame = tk.Frame(root, bg="#f5f7fa")
button_frame.pack(pady=15)

encrypt_btn = tk.Button(
    button_frame,
    text="🔐 Encrypt",
    command=encrypt_gui,
    bg="#1976D2",
    fg="white",
    width=15
)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(
    button_frame,
    text="🔓 Decrypt",
    command=decrypt_gui,
    bg="#FF9800",
    fg="white",
    width=15
)
decrypt_btn.grid(row=0, column=1, padx=10)

# ---------------- Status ----------------

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI", 10),
    bg="#f5f7fa",
    fg="green"
)
status_label.pack(pady=15)

# ---------------- Footer ----------------

footer = tk.Label(
    root,
    text="Developed by Archita Shinde",
    font=("Segoe UI", 9, "italic"),
    bg="#f5f7fa",
    fg="gray"
)
footer.pack(side="bottom", pady=10)

root.mainloop()

root.mainloop()

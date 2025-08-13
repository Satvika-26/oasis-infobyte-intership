import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# Function to evaluate password strength
def evaluate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8:
        score += 1
    if has_upper and has_lower:
        score += 1
    if has_special:
        score += 1
    if repetition_allowed.get() is False:
        score += 1

    if score <= 1:
        return ("Weak", "red")
    elif score == 2 or score == 3:
        return ("Medium", "orange")
    else:
        return ("Strong", "green")

# Generate password function
def generate_password():
    length = password_length.get()

    if length < 6:
        messagebox.showwarning("Weak Password", "Password length should be at least 6 characters.")
        return

    options = []
    if use_uppercase.get():
        options.append(string.ascii_uppercase)
    if use_lowercase.get():
        options.append(string.ascii_lowercase)
    if include_special.get():
        options.append(string.punctuation)

    if not options:
        messagebox.showwarning("No Options Selected", "Please select at least one character type.")
        return

    char_pool = ''.join(options)
    allow_repeat = repetition_allowed.get()

    if not allow_repeat and length > len(set(char_pool)):
        messagebox.showerror("Too Few Unique Characters", 
            "Not enough unique characters to generate password without repetition. Reduce length or allow repetition.")
        return

    if allow_repeat:
        password = [random.choice(char_pool) for _ in range(length)]
    else:
        password = random.sample(char_pool, length)

    # Ensure at least one from each selected category
    guaranteed = [random.choice(opt) for opt in options]
    for i in range(len(guaranteed)):
        password[i] = guaranteed[i]

    random.shuffle(password)
    password_str = ''.join(password)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password_str)

    # Evaluate strength
    strength, color = evaluate_strength(password_str)
    strength_label.config(text=f"Strength: {strength}", fg=color)

# Clipboard copy
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first!")

# GUI setup
root = tk.Tk()
root.title("Advanced Password Generator with Strength Meter")
root.geometry("450x500")
root.config(padx=20, pady=20)

tk.Label(root, text="Advanced Password Generator", font=("Helvetica", 16, "bold")).pack(pady=10)

# Password display
password_entry = tk.Entry(root, font=("Courier", 14), width=30, justify='center')
password_entry.pack(pady=10)

# Strength meter label
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"))
strength_label.pack(pady=5)

# Password length
tk.Label(root, text="Password Length:").pack()
password_length = tk.IntVar(value=12)
tk.Spinbox(root, from_=6, to=32, textvariable=password_length, width=5).pack(pady=5)

# Character options
use_uppercase = tk.BooleanVar(value=True)
use_lowercase = tk.BooleanVar(value=True)
include_special = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase Letters (A-Z)", variable=use_uppercase).pack(anchor='w')
tk.Checkbutton(root, text="Include Lowercase Letters (a-z)", variable=use_lowercase).pack(anchor='w')
tk.Checkbutton(root, text="Include Special Characters (!@#$...)", variable=include_special).pack(anchor='w')

# Repetition control
repetition_allowed = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Allow Repetition of Characters", variable=repetition_allowed).pack(anchor='w', pady=5)

# Action buttons
tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", width=20).pack(pady=15)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white", width=20).pack()

root.mainloop()
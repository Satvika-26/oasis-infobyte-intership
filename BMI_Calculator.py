import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# File to store user data
DATA_FILE = "bmi_data.csv"

# Create file with headers if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Weight", "Height", "BMI"])
    df.to_csv(DATA_FILE, index=False)

# BMI Calculation
def calculate_bmi():
    name = name_entry.get().strip()
    weight = weight_entry.get().strip()
    height = height_entry.get().strip()

    if not name or not weight or not height:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        weight = float(weight)
        height = float(height) / 100  # cm to meters
        bmi = round(weight / (height ** 2), 2)
        result_label.config(text=f"BMI: {bmi}")

        # Save data
        today = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame([[name, today, weight, height * 100, bmi]],
                                columns=["Name", "Date", "Weight", "Height", "BMI"])
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

        messagebox.showinfo("Success", f"BMI calculated and saved for {name}!")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# View history
def view_history():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Enter a name to view history.")
        return

    df = pd.read_csv(DATA_FILE)
    user_data = df[df['Name'].str.lower() == name.lower()]

    if user_data.empty:
        messagebox.showinfo("No Data", f"No history found for {name}.")
        return

    history_window = tk.Toplevel(window)
    history_window.title(f"{name}'s BMI History")

    tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI"), show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in ["Date", "Weight", "Height", "BMI"]:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for _, row in user_data.iterrows():
        tree.insert("", "end", values=(row["Date"], row["Weight"], row["Height"], row["BMI"]))

# Plot BMI trend
def plot_trend():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Input Error", "Enter a name to plot trend.")
        return

    df = pd.read_csv(DATA_FILE)
    user_data = df[df['Name'].str.lower() == name.lower()]

    if user_data.empty:
        messagebox.showinfo("No Data", f"No data to plot for {name}.")
        return

    user_data['Date'] = pd.to_datetime(user_data['Date'])
    user_data = user_data.sort_values('Date')

    plt.figure(figsize=(8, 4))
    plt.plot(user_data['Date'], user_data['BMI'], marker='o', color='blue')
    plt.title(f"{name}'s BMI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# GUI Window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x350")

# Widgets
tk.Label(window, text="Name:").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Weight (kg):").pack()
weight_entry = tk.Entry(window)
weight_entry.pack()

tk.Label(window, text="Height (cm):").pack()
height_entry = tk.Entry(window)
height_entry.pack()

tk.Button(window, text="Calculate BMI", command=calculate_bmi).pack(pady=5)
result_label = tk.Label(window, text="BMI: --", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

tk.Button(window, text="View History", command=view_history).pack(pady=5)
tk.Button(window, text="Plot BMI Trend", command=plot_trend).pack(pady=5)

window.mainloop()

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store user data
DATA_FILE = "users.json"

# Check if the data file exists, if not create one
def initialize_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

# Load user data
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save user data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ATM Interface class
class ATM:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Interface")
        self.root.geometry("400x500")
        self.root.configure(bg="#FFFFFF")  # Modern & Minimalist background
        self.user_data = load_data()
        self.current_user = None
        
        self.create_login_screen()
    
    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root, bg="#E3F2FD", padx=20, pady=20)  # Light Blue frame
        frame.pack(pady=50)
        
        tk.Label(frame, text="Welcome to ATM", font=("Arial", 18), bg="#E3F2FD", fg="#333333").pack(pady=10)
        
        tk.Label(frame, text="Account Number:", bg="#E3F2FD", fg="#333333").pack()
        self.acc_entry = tk.Entry(frame)
        self.acc_entry.pack(pady=5)
        
        tk.Label(frame, text="PIN:", bg="#E3F2FD", fg="#333333").pack()
        self.pin_entry = tk.Entry(frame, show="*")
        self.pin_entry.pack(pady=5)
        
        tk.Button(frame, text="Login", bg="#2196F3", fg="white", command=self.authenticate, padx=10, pady=5).pack(pady=5)
        tk.Button(frame, text="New User? Register", bg="#2196F3", fg="white", command=self.create_registration_screen, padx=10, pady=5).pack(pady=10)
    
    def authenticate(self):
        acc_num = self.acc_entry.get()
        pin = self.pin_entry.get()
        
        if acc_num in self.user_data and self.user_data[acc_num]['pin'] == pin:
            self.current_user = acc_num
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid Account Number or PIN")
    
    def create_registration_screen(self):
        acc_num = simpledialog.askstring("Register", "Enter a new Account Number:")
        if not acc_num or acc_num in self.user_data:
            messagebox.showerror("Error", "Invalid or existing account number!")
            return
        
        pin = simpledialog.askstring("Register", "Set a 4-digit PIN:", show="*")
        if not pin or len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be a 4-digit number!")
            return
        
        self.user_data[acc_num] = {"pin": pin, "balance": 0, "transactions": []}
        save_data(self.user_data)
        messagebox.showinfo("Success", "Account created successfully! You can now log in.")
    
    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root, bg="#E3F2FD", padx=20, pady=20)  # Light Blue frame
        frame.pack(pady=50, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Welcome to ATM", font=("Arial", 16), bg="#E3F2FD", fg="#333333").pack(pady=10)
        tk.Label(frame, text="Main Menu", font=("Arial", 14), bg="#E3F2FD", fg="#333333").pack(pady=5)
        
        buttons = [
            ("Check Balance", self.check_balance),
            ("Deposit Money", self.deposit_money),
            ("Withdraw Money", self.withdraw_money),
            ("Transaction History", self.transaction_history),
            ("Logout", self.create_login_screen)
        ]
        
        for text, command in buttons:
            tk.Button(frame, text=text, bg="#2196F3", fg="white", command=command, padx=10, pady=5, width=30).pack(pady=5, fill=tk.X)
    
    def check_balance(self):
        balance = self.user_data[self.current_user]['balance']
        messagebox.showinfo("Balance", f"Your current balance is ₹{balance}")
    
    def deposit_money(self):
        amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            self.user_data[self.current_user]['balance'] += amount
            self.user_data[self.current_user]['transactions'].append(f"Deposited ₹{amount}")
            save_data(self.user_data)
            messagebox.showinfo("Success", f"₹{amount} deposited successfully!")
        else:
            messagebox.showerror("Error", "Invalid amount!")
    
    def withdraw_money(self):
        amount = simpledialog.askinteger("Withdraw", "Enter amount to withdraw:")
        if amount and 0 < amount <= self.user_data[self.current_user]['balance']:
            self.user_data[self.current_user]['balance'] -= amount
            self.user_data[self.current_user]['transactions'].append(f"Withdrew ₹{amount}")
            save_data(self.user_data)
            messagebox.showinfo("Success", f"₹{amount} withdrawn successfully!")
        else:
            messagebox.showerror("Error", "Insufficient balance or invalid amount!")
    
    def transaction_history(self):
        history = self.user_data[self.current_user]['transactions']
        messagebox.showinfo("Transaction History", "\n".join(history) if history else "No transactions yet.")
    
# Initialize user data
initialize_data()

# Run ATM Interface
if __name__ == "__main__":
    root = tk.Tk()
    app = ATM(root)
    root.mainloop()

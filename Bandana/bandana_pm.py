import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json', master_key_file='master_key.key'):
        self.key_file = key_file
        self.data_file = data_file
        self.master_key_file = master_key_file
        self.load_or_generate_key()
        self.load_or_generate_master_key()

    def load_or_generate_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)

        with open(self.key_file, 'rb') as key_file:
            self.key = key_file.read()

    def load_or_generate_master_key(self):
        if not os.path.exists(self.master_key_file):
            master_key = Fernet.generate_key()
            with open(self.master_key_file, 'wb') as master_key_file:
                master_key_file.write(master_key)

        with open(self.master_key_file, 'rb') as master_key_file:
            self.master_key = master_key_file.read()

    def encrypt_password(self, password):
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        cipher_suite = Fernet(self.key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password

    def register_master_password(self, master_password):
        cipher_suite = Fernet(self.master_key)
        encrypted_master_password = cipher_suite.encrypt(master_password.encode())
        with open('master_password.key', 'wb') as master_password_file:
            master_password_file.write(encrypted_master_password)

    def login_master_password(self, master_password):
        try:
            with open('master_password.key', 'rb') as master_password_file:
                encrypted_master_password = master_password_file.read()
                cipher_suite = Fernet(self.master_key)
                decrypted_master_password = cipher_suite.decrypt(encrypted_master_password).decode()
                return decrypted_master_password == master_password
        except FileNotFoundError:
            return False

    def load_passwords(self):
        data = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    pass
        return data

    def save_passwords(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2, default=lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
            file.write('\n')  # Add a newline for better readability between entries

    def generate_password(self, length=12):
        import secrets
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        return password

    def add_password(self, website, username, password):
        data = self.load_passwords()
        encrypted_password = self.encrypt_password(password)
        if website in data:
            # Check if data[website] is a list, if not, convert it to a list
            if not isinstance(data[website], list):
                data[website] = [data[website]]
            data[website].append({'username': username, 'password': encrypted_password})
        else:
            data[website] = [{'username': username, 'password': encrypted_password}]
        self.save_passwords(data)

    def search_password(self, website):
        data = self.load_passwords()
        if website in data:
            return data[website]
        else:
            return None

class PasswordManagerGUI:
    def __init__(self, password_manager):
        self.password_manager = password_manager

        self.window = tk.Tk()
        self.window.title("Password Manager")

        # Entry fields
        self.master_password_entry = tk.Entry(self.window, width=30, show='*')
        self.website_entry = tk.Entry(self.window, width=30)
        self.username_entry = tk.Entry(self.window, width=30)
        self.password_entry = tk.Entry(self.window, width=30, show='*')

        # Buttons
        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.add_button = tk.Button(self.window, text="Add Password", command=self.add_password)
        self.search_button = tk.Button(self.window, text="Search Password", command=self.search_password)
        self.generate_button = tk.Button(self.window, text="Generate Password", command=self.generate_password)

        # Layout
        self.master_password_entry.grid(row=0, column=1, padx=10, pady=5)
        self.website_entry.grid(row=1, column=1, padx=10, pady=5)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.window, text="Master Password:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Website:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Username:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Password:").grid(row=3, column=0, padx=10, pady=5)

        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.login_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.add_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.generate_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.search_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.logged_in = False

    def register(self):
        master_password = self.master_password_entry.get()

        if master_password:
            self.password_manager.register_master_password(master_password)
            messagebox.showinfo("Registration Success", "Master password registered successfully! You can now login.")
        else:
            messagebox.showwarning("Incomplete Information", "Please enter a master password.")

    def login(self):
        master_password = self.master_password_entry.get()

        if master_password:
            if self.password_manager.login_master_password(master_password):
                self.logged_in = True
                messagebox.showinfo("Login Success", "Logged in successfully!")
            else:
                messagebox.showerror("Login Failed", "Incorrect master password.")
        else:
            messagebox.showwarning("Incomplete Information", "Please enter your master password.")

    def add_password(self):
        if not self.logged_in:
            messagebox.showwarning("Login Required", "Please log in with your master password first.")
            return

        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            self.password_manager.add_password(website, username, password)
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all fields.")

    def search_password(self):
        if not self.logged_in:
            messagebox.showwarning("Login Required", "Please log in with your master password first.")
            return

        website_to_search = self.website_entry.get()

        if website_to_search:
            result = self.password_manager.search_password(website_to_search)
            if result:
                self.display_search_result(result)
            else:
                messagebox.showinfo("Search Result", "Password not found for the given website.")
        else:
            messagebox.showwarning("Incomplete Information", "Please enter a website to search.")

    def display_search_result(self, search_result):
        result_window = tk.Toplevel(self.window)
        result_window.title("Search Result")

        if search_result:
            for password_info in search_result:
                password_label = tk.Label(result_window, text=f"Username: {password_info['username']}\nPassword: {self.password_manager.decrypt_password(password_info['password'])}")
                password_label.pack()

                copy_button = tk.Button(result_window, text="Copy Password", command=lambda password=password_info['password']: self.copy_password(password))
                copy_button.pack()
        else:
            messagebox.showinfo("Search Result", "Password not found for the given website.")

    def generate_password(self):
        if not self.logged_in:
            messagebox.showwarning("Login Required", "Please log in with your master password first.")
            return

        generated_password = self.password_manager.generate_password()
        self.password_entry.delete(0, tk.END)  # Clear existing text
        self.password_entry.insert(0, generated_password)
        messagebox.showinfo("Password Generated", "Password has been generated.")

    def copy_password(self, password):
        decrypted_password = self.password_manager.decrypt_password(password)
        self.window.clipboard_clear()
        self.window.clipboard_append(decrypted_password)
        messagebox.showinfo("Password Copied", "Password has been copied to clipboard.")

    def run(self):
        self.window.mainloop()

password_manager = PasswordManager()
gui = PasswordManagerGUI(password_manager)
gui.run()

# Overview
This Python application provides a secure way to manage passwords using encryption. It features a graphical user interface (GUI) built with Tkinter, allowing users to register, login, add, search, and generate passwords.

# Features
Secure Encryption: Uses cryptography.fernet for encrypting and decrypting passwords.
Master Password: Register and login using a master password to secure your data.
Add Passwords: Store passwords with associated website and username.
Search Passwords: Retrieve stored passwords by specifying the website.
Generate Passwords: Create strong, random passwords.
Copy to Clipboard: Easily copy passwords to the clipboard.
Data Persistence: Passwords and keys are saved in files for future access.

# Usage
# Registering a Master Password
Start the application.
Enter a new master password in the "Master Password" field.
Click "Register".

# Logging In
Enter your master password in the "Master Password" field.
Click "Login".

# Adding a New Password
Log in with your master password.
Enter the website, username, and password in the respective fields.
Click "Add Password".

# Searching for a Stored Password
Log in with your master password.
Enter the website in the "Website" field.
Click "Search Password".
View stored credentials in a new window.

# Generating a Random Password
Log in with your master password.
Click "Generate Password".
The generated password will appear in the "Password" field.

# Copying a Password to Clipboard
Search for a stored password.
In the search result window, click "Copy Password" next to the desired entry.

# Files Created
passwords.json: Stores encrypted passwords.
key.key: Stores the encryption key.
master_key.key: Stores the master key for encrypting the master password.
master_password.key: Stores the encrypted master password.

# Security Note
Ensure to keep your master password safe and never share it.
Regularly backup your .key and .json files to prevent data loss.
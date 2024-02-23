import os
from tkinter import *
import tkinter
import unittest
from unittest.mock import patch
from bandana_pm import PasswordManager,PasswordManagerGUI

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.password_manager = PasswordManager(key_file='test_key.key',
                                                 data_file='test_passwords.json',
                                                 master_key_file='test_master_key.key')

    def tearDown(self):
        if os.path.exists('test_passwords.json'):
            os.remove('test_passwords.json')
        if os.path.exists('test_key.key'):
            os.remove('test_key.key')
        if os.path.exists('test_master_key.key'):
            os.remove('test_master_key.key')

    def test_encrypt_decrypt_password(self):
        password = "test_password"
        encrypted_password = self.password_manager.encrypt_password(password)
        decrypted_password = self.password_manager.decrypt_password(encrypted_password)
        self.assertEqual(decrypted_password, password)
        
    def test_register_login_master_password(self):
        master_password = "test_master_password"
        self.password_manager.register_master_password(master_password)
        self.assertTrue(self.password_manager.login_master_password(master_password))
        
    def test_add_and_search_password(self):
        website = "test_website"
        username = "test_username"
        password = "test_password"
        self.password_manager.add_password(website, username, password)
        search_result = self.password_manager.search_password(website)
        self.assertEqual(search_result[0]['username'], username)
        decrypted_password = self.password_manager.decrypt_password(search_result[0]['password'])
        self.assertEqual(decrypted_password, password)

class TestPasswordManagerGUI(unittest.TestCase):
    def setUp(self):
        self.master = tkinter.Tk()
        self.password_manager = PasswordManager(key_file='test_key.key',
                                                 data_file='test_passwords.json',
                                                 master_key_file='test_master_key.key')
        self.gui = PasswordManagerGUI(self.password_manager)

    def tearDown(self):
        self.master.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_generate_password(self, mocked_showinfo):
        self.gui.logged_in = True
        self.gui.generate_password()
        mocked_showinfo.assert_called_once()

    @patch('tkinter.messagebox.showinfo')
    def test_search_password(self, mocked_showinfo):
        self.gui.logged_in = True
        self.gui.website_entry.insert(0, "test_website")
        self.gui.search_password()
        mocked_showinfo.assert_called_once()

if __name__ == '__main__':
    unittest.main()

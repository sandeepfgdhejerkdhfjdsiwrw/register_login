import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re


def validate_password(password):

    regex = r"^(?=.*[!@#$%^&*()-=_+{}[\]:\"|;'<>,./?])(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$"
    return re.match(regex, password) is not None


class RegistrationForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registration Form")
        self.root.geometry("600x600")  # Set the window size
        self.root.config(bg="light blue")

        self.label_username = tk.Label(self.root, text="Username:", font=("Bold", "20"), bg="light blue")
        self.label_username.place(x='25', y='100')
        self.entry_username = tk.Entry(self.root)
        self.entry_username.place(x='200', y='100', height='35', width='250')

        self.label_password = tk.Label(self.root, text="Password:", font=("Bold", "20"), bg="light blue")
        self.label_password.place(x='25', y='200')
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.place(x='200', y='200', height='35', width='250')

        self.label_email = tk.Label(self.root, text="Email:", font=("Bold", "20"), bg="light blue")
        self.label_email.place(x='25', y='300')
        self.entry_email = tk.Entry(self.root)
        self.entry_email.place(x='200', y='300', height='35', width='250')

        self.button_register = tk.Button(self.root, text="Register", font=("Bold", "20"), activebackground="light blue",
                                         command=self.register)
        self.button_register.place(x='180', y='500')

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="8@Sandeep",
            database="register"
        )

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()

        if username and password and email:
            if len(password) >= 8 and validate_password(password):
                cursor = self.db_connection.cursor()
                query = "INSERT INTO registration (username, password, email) VALUES (%s, %s, %s)"
                values = (username, password, email)
                cursor.execute(query, values)
                self.db_connection.commit()
                cursor.close()
                messagebox.showinfo("Registration Successful", "Username: {}\nPassword: {}\nEmail: {}".format(
                    username, password, email))
                self.root.destroy()
                LoginForm(self.db_connection)
            else:
                messagebox.showerror("Registration Error", "Password should be at least 8 characters long and contain "
                                                           "at least one special character, one uppercase letter, "
                                                           "one lowercase letter, and one digit.")
        else:
            messagebox.showerror("Registration Error", "Please enter all the required information.")

    def __del__(self):
        self.db_connection.close()


class LoginForm:
    def __init__(self, db_connection):
        self.root = tk.Tk()
        self.root.title("Login Form")
        self.root.geometry("500x500")  # Set the window size

        self.label_username = tk.Label(self.root, text="Username:", font=("Bold", "20"))
        self.label_username.place(x='25', y='100')
        self.entry_username = tk.Entry(self.root)
        self.entry_username.place(x='200', y='100', height='35', width='250')

        self.label_password = tk.Label(self.root, text="Password:", font=("Bold", "20"))
        self.label_password.place(x='25', y='200')
        self.entry_password = tk.Entry(self.root)
        self.entry_password.place(x='200', y='200', height='35', width='250')

        self.button_login = tk.Button(self.root, text="Login", font=("Bold", "20"), command=self.login)
        self.button_login.place(x='180', y='300')

        self.db_connection = db_connection

        self.root.mainloop()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            cursor = self.db_connection.cursor()
            query = 'SELECT * FROM registration WHERE username = %s AND password = %s'
            values = (username, password)
            cursor.execute(query, values)
            result = cursor.fetchone()
            cursor.close()

            if result:
                messagebox.showinfo("Login Successful", "Welcome, {}!".format(username))
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")
        else:
            messagebox.showerror("Login Error", "Please enter a username and password.")


if __name__ == "__main__":
    registration_form = RegistrationForm()
    registration_form.root.mainloop()

import tkinter as tk
from tkinter import messagebox
from stock_comparison import StockComparisonApp
import mysql.connector
import bcrypt 

class Logo:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Watcher")
        self.root.geometry("600x200")
        self.setup_login_ui()

    def setup_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Bienvenido", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Iniciar sesión", command=self.setup_login_form, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Registrarse", command=self.setup_register_form, font=("Arial", 12)).pack(pady=5)

    def setup_login_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Correo:").pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        tk.Label(self.root, text="Contraseña:").pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        tk.Button(self.root, text="Entrar", command=self.validate_login).pack(pady=10)

    def setup_register_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Registrar Usuario", font=("Arial", 16)).pack(pady=10)

        self.entry_name = tk.Entry(self.root)
        tk.Label(self.root, text="Nombre:").pack()
        self.entry_name.pack()

        self.entry_lastname = tk.Entry(self.root)
        tk.Label(self.root, text="Apellido:").pack()
        self.entry_lastname.pack()

        self.entry_age = tk.Entry(self.root)
        tk.Label(self.root, text="Edad:").pack()
        self.entry_age.pack()

        self.entry_email = tk.Entry(self.root)
        tk.Label(self.root, text="Correo:").pack()
        self.entry_email.pack()

        self.entry_password = tk.Entry(self.root, show="*")
        tk.Label(self.root, text="Contraseña:").pack()
        self.entry_password.pack()

        tk.Button(self.root, text="Registrar", command=self.register_user).pack(pady=10)

    def validate_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        try:
            connection = mysql.connector.connect(
                user="root",
                password="admin",
                host="localhost",
                database="market_watcher",
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE correo = %s AND contraseña = %s", (email, password))
            user = cursor.fetchone()

            if user:
                self.launch_main_app()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectarse a la base de datos: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def register_user(self):
        name = self.entry_name.get()
        lastname = self.entry_lastname.get()
        age = self.entry_age.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            connection = mysql.connector.connect(
                user="root",
                password="admin",
                host="localhost",
                database="market_watcher",
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (nombre, apellido, edad, correo, contraseña)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, lastname, age, email, hashed_password))
            connection.commit()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.setup_login_ui()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al registrar usuario: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def launch_main_app(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        app = StockComparisonApp(self.root)


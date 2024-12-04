import tkinter as tk
from tkinter import messagebox
from stock_comparison import StockComparisonApp

class Logo:
    def __init__(self, root):
        self.root = root
        # Configurar la ventana raíz
        self.root.title("Market Watcher")
        self.root.geometry("1000x500")  # Tamaño de la ventana
        self.setup_login_ui()

    def setup_login_ui(self):
        # Limpiar la ventana (si ya tenía contenido)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Agregar un mensaje de bienvenida
        label_logo = tk.Label(self.root, text="Bienvenido, introduzca la clave de acceso", font=("Arial", 16))
        label_logo.pack(pady=20, padx=20)

        # Campo para que el usuario introduzca la clave
        self.entry_password = tk.Entry(self.root, show="*", width=20, font=("Arial", 14))
        self.entry_password.pack(pady=10)

        # Botón para validar
        self.btn_submit = tk.Button(self.root, text="Acceder", command=self.validate_password, font=("Arial", 12))
        self.btn_submit.pack(pady=10)

    def validate_password(self):
        password = self.entry_password.get()
        if password == "admin":  # Contraseña predeterminada
            self.launch_main_app()  # Carga la aplicación principal
        else:
            messagebox.showerror("Error", "Clave incorrecta. Inténtalo de nuevo.")

    def launch_main_app(self):
        # Limpiar la ventana y cargar la aplicación principal
        for widget in self.root.winfo_children():
            widget.destroy()

        app = StockComparisonApp(self.root)  # Lanza la aplicación principal
        
        
# Código principal que se ejecuta
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = Logo(root)  # Pasa la ventana principal a la clase Logo
    root.mainloop()  # Llama a mainloop de la ventana principal
import tkinter as tk
from tkinter import ttk
from stock_data import StockDataAPI
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox

# Clase principal para la interfaz gráfica
class StockComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Comparación de Acciones y Usuarios")
        self.root.geometry("900x600")
        self.data_provider = StockDataAPI()

        # Menú
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Agregar comandos al menú
        self.menu_bar.add_command(label="Comparar Acciones", command=self.setup_stock_ui)
        self.menu_bar.add_command(label="Comparar Usuarios", command=self.setup_user_ui)

        # Inicializar la interfaz de comparación de acciones
        self.setup_stock_ui()

    def setup_stock_ui(self):
        self.clear_window()

        # Barra de búsqueda para acciones
        tk.Label(self.root, text="Ingrese los símbolos de acciones (+2, separados por coma):").pack(pady=5)
        self.entry_symbols = tk.Entry(self.root, width=40)
        self.entry_symbols.pack(pady=5)

        # Botón para comparar y graficar
        tk.Button(self.root, text="Comparar y Graficar", command=self.compare_and_plot).pack(pady=10)

        # Barra de búsqueda para usuarios
        tk.Label(self.root, text="Ingrese el nombre o correo del usuario para buscar:").pack(pady=5)
        self.entry_user_search = tk.Entry(self.root, width=40)
        self.entry_user_search.pack(pady=5)

        # Botón para buscar usuarios
        tk.Button(self.root, text="Buscar Usuario", command=self.search_user).pack(pady=10)

        # Tabla para mostrar datos de comparación de acciones
        columns = ("Símbolo", "Precio", "Máximo", "Mínimo", "Volumen")
        self.comparison_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.comparison_tree.heading(col, text=col)
        self.comparison_tree.pack(fill=tk.BOTH, expand=True)

        # Tabla para mostrar usuarios encontrados
        columns_user = ("Usuario", "Correo")
        self.user_tree = ttk.Treeview(self.root, columns=columns_user, show="headings")
        for col in columns_user:
            self.user_tree.heading(col, text=col)
        self.user_tree.pack(fill=tk.BOTH, expand=True)

    def setup_user_ui(self):
        self.clear_window()

        # Barra de búsqueda para usuarios
        tk.Label(self.root, text="Ingrese el nombre o correo del usuario para buscar:").pack(pady=5)
        self.entry_user_search = tk.Entry(self.root, width=40)
        self.entry_user_search.pack(pady=5)

        # Botón para buscar usuarios
        tk.Button(self.root, text="Buscar Usuario", command=self.search_user).pack(pady=10)

        # Tabla para mostrar usuarios encontrados
        columns_user = ("Usuario", "Correo")
        self.user_tree = ttk.Treeview(self.root, columns=columns_user, show="headings")
        for col in columns_user:
            self.user_tree.heading(col, text=col)
        self.user_tree.pack(fill=tk.BOTH, expand=True)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def compare_and_plot(self):
        symbols = self.entry_symbols.get().split(",")
        if len(symbols) < 2:
            messagebox.showwarning("Advertencia", "Ingrese al menos dos símbolos de acciones.")
            return

        comparison_data = []
        historical_data = []
        for symbol in symbols:
            data = self.data_provider.get_stock_data(symbol.strip().upper())
            if data:
                comparison_data.append(data)
                history = self.data_provider.get_historical_data(symbol.strip().upper())
                if history:
                    historical_data.append((symbol.strip().upper(), history))

        self.update_comparison_table(comparison_data)

        if len(historical_data) < 2:
           # messagebox.showinfo("Información", "No hay suficientes datos históricos para graficar.")
            return

        self.plot_comparison_in_new_window(
            historical_data[0][1], historical_data[1][1],
            historical_data[0][0], historical_data[1][0]
        )

    def update_comparison_table(self, data):
        for row in self.comparison_tree.get_children():
            self.comparison_tree.delete(row)
        for stock in data:
            self.comparison_tree.insert("", "end", values=(
                stock["symbol"], stock["price"], stock["high"], stock["low"], stock["volume"]
            ))

    def plot_comparison_in_new_window(self, data1, data2, symbol1, symbol2):
        try:
            times1, prices1 = zip(*data1)
            times2, prices2 = zip(*data2)

            graph_window = tk.Toplevel(self.root)
            graph_window.title("Gráfico de Comparación")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(times1, prices1, label=symbol1, color="blue")
            ax.plot(times2, prices2, label=symbol2, color="red")
            ax.set_title("Comparación de Acciones")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Precio")
            ax.legend()

            step = max(len(times1) // 10, 1)
            ax.set_xticks(times1[::step])
            ax.set_xticklabels(times1[::step], rotation=45, fontsize=8)

            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            tk.Button(graph_window, text="Cerrar", command=graph_window.destroy).pack(pady=10)
        except Exception as e:
            print(f"Error al generar el gráfico: {e}")

    def search_user(self):
        search_term = self.entry_user_search.get()

        try:
            connection = mysql.connector.connect(
                user="root",
                password="admin",
                host="localhost",
                database="market_watcher",
                port=3306
            )
            cursor = connection.cursor()
            query = """
                SELECT id, CONCAT(nombre, ' ', apellido) AS usuario, correo
                FROM users
                WHERE nombre LIKE %s OR correo LIKE %s
            """
            search_like = f"%{search_term}%"
            cursor.execute(query, (search_like, search_like))
            users = cursor.fetchall()

            # Mostrar los resultados en la interfaz
            for row in self.user_tree.get_children():
                self.user_tree.delete(row)
        
            for user in users:
                self.user_tree.insert("", "end", values=(user[1], user[2]))

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar usuario: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


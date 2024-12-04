import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
from stock_data import StockDataAPI

class StockComparisonApp:
    def __init__(self, root, language="en"):
        self.root = root
        self.language = language  # Determina el idioma (español o inglés)
        self.data_provider = StockDataAPI()
        self.setup_ui()

    def setup_ui(self):
        # Textos según el idioma
        if self.language == "es":
            label_symbols = "Ingrese los símbolos de acciones (+ 2 --> separados por coma):"
            btn_compare_text = "Comparar y Graficar"
            columns = ("Símbolo", "Precio", "Máximo", "Mínimo", "Volumen")
        else:
            label_symbols = "Enter stock symbols (+ 2 --> comma-separated):"
            btn_compare_text = "Compare and Plot"
            columns = ("Symbol", "Price", "High", "Low", "Volume")

        # Configuración de la interfaz
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text=label_symbols).pack(side=tk.LEFT, padx=5)
        self.entry_symbols = tk.Entry(frame_top, width=40)
        self.entry_symbols.pack(side=tk.LEFT, padx=5)

        btn_compare = tk.Button(frame_top, text=btn_compare_text, command=self.compare_and_plot)
        btn_compare.pack(side=tk.LEFT, padx=5)

        # Tabla de comparación
        self.comparison_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.comparison_tree.heading(col, text=col)
        self.comparison_tree.pack(fill=tk.BOTH, expand=True)

    def update_comparison_table(self, data):
        for row in self.comparison_tree.get_children():
            self.comparison_tree.delete(row)
        for stock in data:
            self.comparison_tree.insert("", "end", values=(stock["symbol"], stock["price"], stock["high"], stock["low"], stock["volume"]))

    def compare_and_plot(self):
        symbols = self.entry_symbols.get().split(",")  # Obtener los símbolos de las acciones ingresadas
        comparison_data = []

        # Obtener datos de las acciones ingresadas
        for symbol in symbols:
            data = self.data_provider.get_stock_data(symbol.strip().upper())  # Limpiar espacios y convertir a mayúsculas
            if data:
                comparison_data.append(data)

        # Actualizar la tabla con los datos de las acciones
        self.update_comparison_table(comparison_data)

        # Si hay acciones para graficar
        if comparison_data:
            historical_data = []
            colors = self.generate_random_colors(len(comparison_data))  # Generamos colores aleatorios

            for stock_data in comparison_data:
                data = self.data_provider.get_historical_data(stock_data["symbol"])
                print(f"Datos históricos para {stock_data['symbol']}: {data}")  # Verificar los datos obtenidos
                if data:  # Verificar que se obtuvieron datos
                    historical_data.append(data)
                else:
                    print(f"No se obtuvieron datos históricos para {stock_data['symbol']}")

            if historical_data:  # Verificar que tenemos datos históricos para graficar
                self.plot_comparison_in_new_window(historical_data, [stock["symbol"] for stock in comparison_data], colors)
            else:
                print("No se obtuvieron datos históricos para graficar.")

    def plot_comparison_in_new_window(self, historical_data, symbols, colors):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Gráfico de Comparación de Acciones")
        graph_window.geometry("800x800")

        fig, ax = plt.subplots(figsize=(10, 5))

        # Graficar todas las acciones con colores aleatorios
        for i, data in enumerate(historical_data):
            times, prices = zip(*data)

            # Verificar que los datos tienen la longitud correcta antes de graficar
            if len(times) == len(prices):
                ax.plot(times, prices, label=symbols[i], color=colors[i])
            else:
                print(f"Error en los datos de {symbols[i]}: el número de tiempos y precios no coincide.")

        ax.set_title("Comparación de Acciones")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Precio")
        ax.legend()

        # Ajustar las marcas del eje X
        step = max(len(times) // 10, 1)  # Mostrar solo algunas marcas del eje X
        ax.set_xticks(times[::step])
        ax.set_xticklabels(times[::step], rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        close_button = tk.Button(graph_window, text="Cerrar", command=graph_window.destroy)
        close_button.pack(pady=10)

    def generate_random_colors(self, n):
        # Generar una lista de colores aleatorios
        colors = []
        for _ in range(n):
            color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            colors.append(color)
        return colors

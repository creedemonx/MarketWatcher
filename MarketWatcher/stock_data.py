# /src/stock_comparison_app.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests

# Clase para gestionar datos de la API
class StockDataAPI:
    BASE_URL = "https://www.alphavantage.co/query" # --> of course you can change the API for other of your preference 
    API_KEY = "2DRFBD2DK77S6QGW" # --> this is just an example of API KEY, it can be changed

    def get_stock_data(self, symbol):
        try:
            response = requests.get(self.BASE_URL, params={
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": "1min",
                "apikey": self.API_KEY
            })
            response.raise_for_status()
            data = response.json()

            time_series = data.get("Time Series (1min)")
            if not time_series:
                return None

            latest_time = sorted(time_series.keys())[0]
            latest_data = time_series[latest_time]
            return {
                "symbol": symbol,
                "price": float(latest_data["1. open"]),
                "high": float(latest_data["2. high"]),
                "low": float(latest_data["3. low"]),
                "volume": int(latest_data["5. volume"])
            }
        except Exception as e:
            print(f"Error al obtener datos para {symbol}: {e}")
            return None

    def get_historical_data(self, symbol):
        try:
            response = requests.get(self.BASE_URL, params={
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": "1min",
                "apikey": self.API_KEY
            })
            response.raise_for_status()
            data = response.json()

            time_series = data.get("Time Series (1min)")
            if not time_series:
                return []

            sorted_data = sorted(time_series.items())  # Ordenar por tiempo
            times = [entry[0] for entry in sorted_data]
            prices = [float(entry[1]["1. open"]) for entry in sorted_data]
            return list(zip(times, prices))
        except Exception as e:
            print(f"Error al obtener datos históricos para {symbol}: {e}")
            return []

# App Controller
class StockComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación de Acciones")
        self.root.geometry("800x400")

        self.data_provider = StockDataAPI()
        self.setup_ui()

    def setup_ui(self):
        # Entry for comparators symbols
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Ingrese los símbolos de acciones (separados por coma):").pack(side=tk.LEFT, padx=5)
        self.entry_symbols = tk.Entry(frame_top, width=40)
        self.entry_symbols.pack(side=tk.LEFT, padx=5)

        btn_compare = tk.Button(
            frame_top, text="Comparar y Graficar",
            command=self.compare_and_plot
        )
        btn_compare.pack(side=tk.LEFT, padx=5)

        # Entry for search an additional share 
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=10)

        tk.Label(frame_bottom, text="Ingrese otro símbolo de acción para buscar:").pack(side=tk.LEFT, padx=5)
        self.entry_symbol_new = tk.Entry(frame_bottom, width=40)
        self.entry_symbol_new.pack(side=tk.LEFT, padx=5)

        btn_search_new = tk.Button(
            frame_bottom, text="Buscar otra acción",
            command=self.search_another_stock
        )
        btn_search_new.pack(side=tk.LEFT, padx=5)

        # Tabla de comparación
        columns = ("Símbolo", "Precio", "Máximo", "Mínimo", "Volumen")
        self.comparison_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.comparison_tree.heading(col, text=col)
        self.comparison_tree.pack(fill=tk.BOTH, expand=True)

    def update_comparison_table(self, data):
        for row in self.comparison_tree.get_children():
            self.comparison_tree.delete(row)
        for stock in data:
            self.comparison_tree.insert("", "end", values=(
                stock["symbol"], stock["price"], stock["high"], stock["low"], stock["volume"]
            ))

    def plot_comparison_in_new_window(self, data1, data2, symbol1, symbol2):
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Gráfico de Comparación de Acciones")
        graph_window.geometry("800x800")

        times1, prices1 = zip(*data1)
        times2, prices2 = zip(*data2)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(times1, prices1, label=symbol1, color="blue")
        ax.plot(times2, prices2, label=symbol2, color="red")
        ax.set_title("Comparación de Acciones")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Precio")
        ax.legend()

        step = max(len(times1) // 10, 1)
        ax.set_xticks(times1[::step])
        ax.set_xticklabels(times1[::step], rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        close_button = tk.Button(graph_window, text="Cerrar", command=graph_window.destroy)
        close_button.pack(pady=10)

    def compare_and_plot(self):
        symbols = self.entry_symbols.get().split(",")
        comparison_data = []

        for symbol in symbols:
            data = self.data_provider.get_stock_data(symbol.strip().upper())
            if data:
                comparison_data.append(data)

        self.update_comparison_table(comparison_data)

        if len(comparison_data) == 2:
            data1 = self.data_provider.get_historical_data(comparison_data[0]["symbol"])
            data2 = self.data_provider.get_historical_data(comparison_data[1]["symbol"])
            self.plot_comparison_in_new_window(
                data1, data2, comparison_data[0]["symbol"], comparison_data[1]["symbol"]
            )

    def search_another_stock(self):
        symbol = self.entry_symbol_new.get().strip().upper()
        data = self.data_provider.get_stock_data(symbol)
        if data:
            print(f"Datos obtenidos para {symbol}: {data}")
            self.update_comparison_table([data])
        else:
            print(f"No se pudieron obtener datos para {symbol}")


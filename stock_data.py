import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import yfinance as yf  # type: ignore

# Clase para gestionar datos de Yahoo Finance
class StockDataAPI:
    def get_stock_data(self, symbol):
        try:
            # Usando yfinance para obtener los datos actuales de la acción
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")  # Se obtienen solo los datos del día actual

            if not data.empty:
                latest_data = data.iloc[-1]  # El último valor disponible
                return {
                    "symbol": symbol,
                    "price": latest_data["Close"],
                    "high": latest_data["High"],
                    "low": latest_data["Low"],
                    "volume": latest_data["Volume"]
                }
            else:
                print(f"No se encontraron datos para {symbol}.")
                return None
        except (ValueError, Exception) as e:
            print(f"Error al obtener datos para {symbol}: {e}")
            return None

    def get_historical_data(self, symbol):
        try:
            # Usamos yfinance para obtener los datos históricos de la acción
            stock = yf.Ticker(symbol)
            historical_data = stock.history(period="1mo")  # Último mes de datos

            if historical_data.empty:
                print(f"No hay datos históricos disponibles para {symbol}")
                return []

            times = historical_data.index.strftime("%Y-%m-%d").tolist()  # Fechas
            prices = historical_data["Close"].tolist()  # Precios de cierre
            return list(zip(times, prices))
        except (ValueError, Exception) as e:
            print(f"Error al obtener datos históricos para {symbol}: {e}")
            return []

# Controlador de la aplicación
class StockComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparación de Acciones")
        self.root.geometry("800x400")

        self.data_provider = StockDataAPI()
        self.setup_ui()

    def setup_ui(self):
        # Entrada para los símbolos de las acciones a comparar
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Ingrese los símbolos de acciones (separados por coma):").pack(side=tk.LEFT, padx=5)
        self.entry_symbols = tk.Entry(frame_top, width=40)
        self.entry_symbols.pack(side=tk.LEFT, padx=5)

        btn_compare = tk.Button(
            frame_top, text="Comparar y hacer gráfico", command=self.compare_and_plot
        )
        btn_compare.pack(side=tk.LEFT, padx=5)

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

        # Ajustar las etiquetas para evitar superposición
        step = max(len(times1) // 10, 1)
        ax.set_xticks(times1[::step])
        ax.set_xticklabels(times1[::step], rotation=45, fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        close_button = tk.Button(graph_window, text="Cerrar", command=graph_window.destroy)
        close_button.pack(pady=10)

    def compare_and_plot(self):
        symbols = self.entry_symbols.get().strip()
        if not symbols:
            print("Por favor, ingrese al menos un símbolo de acción.")
            return

        symbols = symbols.split(",")
        comparison_data = []

        for symbol in symbols:
            data = self.data_provider.get_stock_data(symbol.strip().upper())
            if data:
                comparison_data.append(data)

        self.update_comparison_table(comparison_data)

        if len(comparison_data) < 2:
            print("Se necesitan al menos dos símbolos válidos para comparar y graficar.")
            return

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


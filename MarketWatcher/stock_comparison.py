# stock_comparison_app.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from stock_data_api import StockDataAPI

class StockComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarketWatcher")
        self.root.geometry("800x400")

        self.data_provider = StockDataAPI()
        self.setup_ui()

    def setup_ui(self):
        # Entrada para los símbolos de comparación
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Enter stock symbols (comma-separated):").pack(side=tk.LEFT, padx=5)
        self.entry_symbols = tk.Entry(frame_top, width=40)
        self.entry_symbols.pack(side=tk.LEFT, padx=5)

        btn_compare = tk.Button(
            frame_top, text="Compare and Plot",
            command=self.compare_and_plot
        )
        btn_compare.pack(side=tk.LEFT, padx=5)

        # Entrada para buscar una acción adicional
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=10)

        tk.Label(frame_bottom, text="Enter a stock symbol to search:").pack(side=tk.LEFT, padx=5)
        self.entry_symbol_new = tk.Entry(frame_bottom, width=40)
        self.entry_symbol_new.pack(side=tk.LEFT, padx=5)

        btn_search_new = tk.Button(
            frame_bottom, text="Search Stock",
            command=self.search_another_stock
        )
        btn_search_new.pack(side=tk.LEFT, padx=5)

        # Tabla de comparación
        columns = ("Symbol", "Price", "High", "Low", "Volume")
        self.comparison_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.comparison_tree.heading(col, text=col)
        self.comparison_tree.pack(fill=tk.BOTH, expand=True)

    def update_comparison_table(self, data):
        for row in self.comparison_tree.get_ch

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 22:14:21 2024

@author: geja2
"""

# main.py
import tkinter as tk
from stock_comparison_app import StockComparisonApp

if __name__ == "__main__":
    root = tk.Tk()
    app = StockComparisonApp(root)
    root.mainloop()

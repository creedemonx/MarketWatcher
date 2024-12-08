import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import yfinance as yf  # type: ignore
import mysql.connector

class StockDataAPI:
    def get_stock_data(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                latest_data = data.iloc[-1]
                return {
                    "symbol": symbol,
                    "price": latest_data["Close"],
                    "high": latest_data["High"],
                    "low": latest_data["Low"],
                    "volume": latest_data["Volume"]
                }
            print(f"No se encontraron datos para {symbol}.")
            return None
        except Exception as e:
            print(f"Error al obtener datos para {symbol}: {e}")
            return None

    def get_historical_data(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1mo")
            if not data.empty:
                times = data.index.strftime("%Y-%m-%d").tolist()
                prices = data["Close"].tolist()
                return list(zip(times, prices))
            print(f"No hay datos históricos para {symbol}")
            return []
        except Exception as e:
            print(f"Error al obtener datos históricos para {symbol}: {e}")
            return []

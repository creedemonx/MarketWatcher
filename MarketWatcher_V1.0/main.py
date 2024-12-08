# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 22:14:21 2024 
@author: geja2
"""
# main.py
import tkinter as tk
from logo import Logo  
from stock_comparison import StockComparisonApp  
#from user_comparison import UserComparisonApp 
# Clase principal para iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Market Watcher - Aplicación de Comparación de Acciones y Usuarios")
    root.geometry("800x600")  
    # Lanza la pantalla de inicio (Logo) primero
    app = Logo(root)
    # Inicia el bucle principal de la interfaz gráfica de usuario
    root.mainloop()

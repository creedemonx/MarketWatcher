# Documentación de MarketWatcher 
#ENGLISH BELOW 

El código implementa una aplicación de escritorio llamada **MarketWatcher**, que permite la comparación de datos bursátiles y la visualización de gráficos históricos para acciones seleccionadas. Está estructurado en dos clases principales: `StockDataAPI`, para la gestión de datos financieros desde la API de **Alpha Vantage**, y `StockComparisonApp`, para la configuración y control de la interfaz gráfica de usuario.

---

### **Clases y Funcionalidades**

### **1. Clase `StockDataAPI`**

Encargada de interactuar con la API de Alpha Vantage para obtener datos financieros. Contiene métodos para recuperar información actual e histórica de acciones.

### **Métodos:**

1. **`get_stock_data(symbol: str) -> dict`**
    - Realiza una solicitud a la API para obtener los datos más recientes de una acción específica.
    - Procesa la respuesta JSON para extraer información como:
        - Precio de apertura (`open`).
        - Precio máximo (`high`).
        - Precio mínimo (`low`).
        - Volumen negociado (`volume`).
    - Devuelve un diccionario con estos datos o `None` si no se encuentra información para el símbolo proporcionado.
2. **`get_historical_data(symbol: str) -> list`**
    - Solicita datos históricos con intervalos de 1 minuto para el símbolo especificado.
    - Extrae y organiza los datos en una lista de tuplas, cada una con un tiempo y el precio correspondiente.
    - Retorna una lista vacía en caso de errores o ausencia de datos.

---

### **2. Clase `StockComparisonApp`**

Define la interfaz gráfica de la aplicación y gestiona las interacciones del usuario. Se conecta con la clase `StockDataAPI` para obtener datos y mostrarlos en la interfaz.

### **Atributos:**

1. **`root`**: Instancia de la ventana principal de Tkinter.
2. **`data_provider`**: Instancia de `StockDataAPI` para la gestión de datos financieros.
3. **`entry_symbols`**: Campo de entrada para ingresar los símbolos de las acciones a comparar.
4. **`entry_symbol_new`**: Campo de entrada para buscar información de un símbolo adicional.
5. **`comparison_tree`**: Tabla interactiva para visualizar los datos de las acciones seleccionadas.

### **Métodos:**

1. **`__init__(root: tk.Tk)`**
    - Configura la ventana principal de la aplicación.
    - Inicializa los elementos de la interfaz gráfica, como los campos de entrada, botones y la tabla.
2. **`setup_ui()`**
    - Configura los widgets de la interfaz:
        - Entrada de texto para ingresar múltiples símbolos de acciones.
        - Botones para comparar y buscar datos.
        - Tabla interactiva para mostrar los resultados de las consultas.
3. **`update_comparison_table(data: list)`**
    - Limpia y actualiza las filas de la tabla con nuevos datos proporcionados.
    - Cada fila representa una acción, mostrando:
        - Símbolo.
        - Precio de apertura.
        - Precio máximo.
        - Precio mínimo.
        - Volumen negociado.
4. **`plot_comparison_in_new_window(data1: list, data2: list, symbol1: str, symbol2: str)`**
    - Abre una nueva ventana para mostrar un gráfico comparativo de dos acciones.
    - Utiliza los datos históricos proporcionados para trazar dos líneas:
        - La primera en color azul para la acción `symbol1`.
        - La segunda en color rojo para la acción `symbol2`.
    - Configura etiquetas y rota las marcas del eje X para mejorar la legibilidad.
5. **`compare_and_plot()`**
    - Obtiene los datos actuales de los símbolos ingresados por el usuario.
    - Si hay al menos dos símbolos, solicita sus datos históricos y genera un gráfico comparativo.
    - Actualiza la tabla con los datos más recientes.
6. **`search_another_stock()`**
    - Busca información para un símbolo adicional ingresado en un campo específico.
    - Inserta los datos obtenidos en la tabla, mostrando solo la acción buscada.

---

### **Flujo de ejecución**

1. **Inicio de la aplicación:**
    - El script inicia creando una instancia de `StockComparisonApp`, configurando la ventana principal y sus componentes.
2. **Ingreso de símbolos:**
    - El usuario ingresa los símbolos de las acciones en el campo correspondiente.
    - Al hacer clic en el botón **"Comparar y Graficar"**, el programa obtiene los datos actuales de las acciones y los muestra en la tabla.
    - Si hay al menos dos símbolos, se genera un gráfico en una ventana secundaria.
3. **Búsqueda de un símbolo adicional:**
    - El usuario puede ingresar un símbolo en un campo adicional.
    - Al hacer clic en el botón **"Buscar otra acción"**, el programa muestra la información del símbolo en la tabla.
4. **Visualización de gráficos:**
    - Los gráficos muestran las tendencias históricas de los precios de apertura para los dos símbolos seleccionados.
    - Se configura una rotación de las marcas del eje X para mejorar la presentación de los datos.

---

### **Comportamiento esperado**

- **Datos válidos:** Los símbolos correctamente ingresados muestran información actual en la tabla y generan gráficos si se seleccionan dos.
- **Errores manejados:** Si los datos no están disponibles (por ejemplo, símbolo incorrecto o límite de la API), el programa imprime un mensaje informativo y no afecta la interfaz.

Este diseño permite una interacción fluida entre el usuario y los datos financieros, integrando de manera eficiente la interfaz gráfica con la obtención de información en tiempo real.

---

ENGLISH VERSION : 

### **Detailed Description of the Code**

The code implements a desktop application called **MarketWatcher**, designed to allow users to compare stock market data and visualize historical trends for selected stocks. It is structured into two main classes: `StockDataAPI`, which handles financial data retrieval via the **Alpha Vantage** API, and `StockComparisonApp`, which manages the graphical user interface (GUI) and user interactions.

---

### **Classes and Functionalities**

### **1. Class `StockDataAPI`**

This class handles interactions with the Alpha Vantage API to fetch financial data. It provides methods to retrieve both current and historical stock data.

### **Methods:**

1. **`get_stock_data(symbol: str) -> dict`**
    - Sends a request to the API to fetch the most recent data for a specific stock.
    - Processes the JSON response to extract information such as:
        - Opening price (`open`).
        - Highest price (`high`).
        - Lowest price (`low`).
        - Trading volume (`volume`).
    - Returns a dictionary containing this data or `None` if no data is found for the given symbol.
2. **`get_historical_data(symbol: str) -> list`**
    - Fetches historical data with 1-minute intervals for the specified stock symbol.
    - Extracts and organizes the data into a list of tuples, each containing a timestamp and its corresponding price.
    - Returns an empty list if an error occurs or no data is available.

---

### **2. Class `StockComparisonApp`**

This class defines the application's graphical user interface (GUI) and connects user inputs with data processing and visualization functionalities.

### **Attributes:**

1. **`root`**: The main Tkinter window instance.
2. **`data_provider`**: An instance of `StockDataAPI` to manage financial data.
3. **`entry_symbols`**: Input field for entering stock symbols to compare.
4. **`entry_symbol_new`**: Input field for searching additional stock information.
5. **`comparison_tree`**: A table widget for displaying stock data.

### **Methods:**

1. **`__init__(root: tk.Tk)`**
    - Sets up the main application window.
    - Initializes all GUI components, including buttons, input fields, and the data table.
2. **`setup_ui()`**
    - Configures all widgets for the user interface:
        - Input fields for entering stock symbols.
        - Buttons for comparison and search functionalities.
        - A table to display stock data.
3. **`update_comparison_table(data: list)`**
    - Clears the existing table and updates it with new data.
    - Each row represents a stock, displaying:
        - Symbol.
        - Opening price.
        - Highest price.
        - Lowest price.
        - Trading volume.
4. **`plot_comparison_in_new_window(data1: list, data2: list, symbol1: str, symbol2: str)`**
    - Opens a new window to display a comparison chart of two stocks.
    - Plots two lines:
        - The first in blue for `symbol1`.
        - The second in red for `symbol2`.
    - Configures axis labels and rotates X-axis tick labels for better readability.
5. **`compare_and_plot()`**
    - Fetches current data for the symbols entered by the user.
    - If at least two symbols are provided, retrieves their historical data and generates a comparison chart.
    - Updates the table with the latest data.
6. **`search_another_stock()`**
    - Fetches data for an additional stock entered in a separate input field.
    - Updates the table to display the retrieved data for the specific stock.

---

### **Execution Flow**

1. **Application Launch:**
    - The script starts by creating an instance of `StockComparisonApp`, setting up the main window and its components.
2. **Entering Symbols:**
    - Users input stock symbols in the designated field.
    - Clicking the **"Compare and Plot"** button fetches the latest data and updates the table.
    - If two symbols are entered, a chart comparing their historical data is generated.
3. **Searching for Additional Stocks:**
    - Users can input a symbol in the secondary field.
    - Clicking the **"Search Another Stock"** button displays the data for the specified stock in the table.
4. **Chart Visualization:**
    - The chart shows historical trends for the opening prices of two selected stocks.
    - The X-axis labels are rotated for better readability.

---

### **Expected Behavior**

- **Valid Data:** Correctly entered symbols display the latest stock data in the table and generate charts when two symbols are selected.
- **Error Handling:** If no data is available (e.g., due to an invalid symbol or API limit), the program prints an error message and ensures the GUI remains unaffected.

This design provides a seamless interaction between the user and financial data, efficiently integrating GUI elements with real-time stock market information.

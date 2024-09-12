import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import webbrowser
import requests
from PIL import Image, ImageTk
import json

# Conversión de peso colombiano a dólares
COP_TO_USD = 0.00024

# Diccionario con multiplicadores por estrato
estrato_multiplicadores = {
    1: 0.7,
    2: 0.8,
    3: 0.9,
    4: 1.0,
    5: 1.2,
    6: 1.5
}

def obtener_precio_en_moneda_local(precio_usd, codigo_pais):
    api_key = "99cf1eb7c34ff70da08a45a2"
    url = f"https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    if codigo_pais in data['rates']:
        tasa_cambio = data['rates'][codigo_pais]
        return precio_usd * tasa_cambio
    else:
        return precio_usd

def ajustar_precio_por_estrato(precio_base_cop, estrato):
    if estrato not in estrato_multiplicadores:
        raise ValueError("Estrato no válido. Debe estar entre 1 y 6.")
    
    # Ajustar precio según estrato
    precio_ajustado = precio_base_cop * estrato_multiplicadores[estrato]
    
    # Convertir a dólares
    precio_en_dolares = precio_ajustado * COP_TO_USD
    
    return precio_ajustado, precio_en_dolares

def guardar_datos():
    direccion = entrada_direccion.get()
    ano_construccion = entrada_ano.get()
    num_pisos = entrada_pisos.get()
    tam_lote = entrada_lote.get()
    num_habitaciones = entrada_habitaciones.get()
    num_banos = entrada_banos.get()
    superficie = entrada_superficie.get()
    tipo_construccion = entrada_tipo.get()
    estado = entrada_estado.get()
    garaje = var_garaje.get()
    piscina = var_piscina.get()
    jardin = var_jardin.get()

    # Estrato de la vivienda (esto ahora viene del formulario)
    estrato = int(entrada_estrato.get())  # Se añade este campo al formulario
    precio_base_cop = 200_000_000  # Precio base en COP (ejemplo)
    
    # Ajustar precio por estrato y convertir a USD
    precio_ajustado_cop, precio_usd = ajustar_precio_por_estrato(precio_base_cop, estrato)

    # Obtener el código del país (debe ser determinado por la dirección o coordenadas)
    codigo_pais = "COP"  # Ejemplo para Colombia
    precio_local = obtener_precio_en_moneda_local(precio_usd, codigo_pais)
    
    archivo_csv = "data/datos_vivienda.csv"
    archivo_existe = os.path.isfile(archivo_csv)
    
    with open(archivo_csv, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        if not archivo_existe:
            escritor.writerow(["Direccion", "Ano Construccion", "Numero Pisos", "Tamano Lote", "Numero Habitaciones", "Numero Banos", "Superficie Construida", "Tipo Construccion", "Estado", "Garaje", "Piscina", "Jardin", "Precio USD", "Precio Local", "Estrato"])
        escritor.writerow([direccion, ano_construccion, num_pisos, tam_lote, num_habitaciones, num_banos, superficie, tipo_construccion, estado, garaje, piscina, jardin, precio_usd, precio_local, estrato])
    
    messagebox.showinfo("Información", f"Datos guardados exitosamente!\nPrecio en COP ajustado: {precio_ajustado_cop}\nPrecio en USD: {precio_usd}\nPrecio en moneda local: {precio_local}")

def capturar_ubicacion():
    ruta_mapa = 'C:/Users/USUARIO/OneDrive/Escritorio/Proyecto_IA/mapa.html'
    webbrowser.open('file://' + os.path.realpath(ruta_mapa))

def recibir_datos_mapa():
    try:
        if os.path.isfile('location_data.txt'):
            with open('location_data.txt', 'r') as file:
                data = json.load(file)
                direccion = data.get('direccion', "")  
                
                entrada_direccion.delete(0, tk.END)
                entrada_direccion.insert(0, direccion)
        else:
            entrada_direccion.delete(0, tk.END)
            entrada_direccion.insert(0, "")  
    except Exception as e:
        print(f"Error al leer los datos del archivo: {e}")
        entrada_direccion.delete(0, tk.END)
        entrada_direccion.insert(0, "")  

def cargar_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg;*.png;*.gif")])
    if ruta_imagen:
        img = Image.open(ruta_imagen)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        
        ventana_imagen = tk.Toplevel()
        ventana_imagen.title("Imagen Cargada")
        label_imagen = tk.Label(ventana_imagen, image=img_tk)
        label_imagen.image = img_tk
        label_imagen.pack()
        
        print(f"Imagen cargada: {ruta_imagen}")

def crear_formulario():
    ventana = tk.Tk()
    ventana.title("Formulario de Evaluación de Vivienda")
    
    etiquetas = [
        "Dirección:",
        "Año de Construcción:",
        "Número de Pisos:",
        "Tamaño del Lote (m²):",
        "Número de Habitaciones:",
        "Número de Baños:",
        "Superficie Construida (m²):",
        "Tipo de Construcción:",
        "Estado General:",
        "Estrato:"
    ]
    
    entradas = {}
    for i, texto in enumerate(etiquetas):
        label = tk.Label(ventana, text=texto)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(ventana)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        entradas[texto] = entrada
    
    global entrada_direccion, entrada_ano, entrada_pisos, entrada_lote, entrada_habitaciones, entrada_banos, entrada_superficie, entrada_tipo, entrada_estado, entrada_estrato
    entrada_direccion = entradas["Dirección:"]
    entrada_ano = entradas["Año de Construcción:"]
    entrada_pisos = entradas["Número de Pisos:"]
    entrada_lote = entradas["Tamaño del Lote (m²):"]
    entrada_habitaciones = entradas["Número de Habitaciones:"]
    entrada_banos = entradas["Número de Baños:"]
    entrada_superficie = entradas["Superficie Construida (m²):"]
    entrada_tipo = entradas["Tipo de Construcción:"]
    entrada_estado = entradas["Estado General:"]
    entrada_estrato = entradas["Estrato:"]  # Nueva entrada para el estrato
    
    global var_garaje, var_piscina, var_jardin
    var_garaje = tk.BooleanVar()
    var_piscina = tk.BooleanVar()
    var_jardin = tk.BooleanVar()
    
    tk.Checkbutton(ventana, text="Garaje", variable=var_garaje).grid(row=len(etiquetas), column=0, columnspan=2, padx=10, pady=5)
    tk.Checkbutton(ventana, text="Piscina", variable=var_piscina).grid(row=len(etiquetas)+1, column=0, columnspan=2, padx=10, pady=5)
    tk.Checkbutton(ventana, text="Jardín", variable=var_jardin).grid(row=len(etiquetas)+2, column=0, columnspan=2, padx=10, pady=5)

    boton_capturar_ubicacion = tk.Button(ventana, text="Capturar Ubicación", command=capturar_ubicacion)
    boton_capturar_ubicacion.grid(row=len(etiquetas), column=0, columnspan=2, pady=10)
    
    boton_cargar_imagen = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
    boton_cargar_imagen.grid(row=len(etiquetas)+1, column=0, columnspan=2, pady=10)
    
    boton_guardar = tk.Button(ventana, text="Guardar Datos", command=guardar_datos)
    boton_guardar.grid(row=len(etiquetas)+2, column=0, columnspan=2, pady=10)
    
    # Cargar dirección desde el archivo
    recibir_datos_mapa()
    
    ventana.mainloop()

if __name__ == "__main__":
    crear_formulario()
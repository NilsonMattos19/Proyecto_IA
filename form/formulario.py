import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os

def guardar_datos():
    # Recopilar datos del formulario
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

    # Nombre del archivo CSV
    archivo_csv = "data/datos_vivienda.csv"
    
    # Verificar si el archivo CSV ya existe
    archivo_existe = os.path.isfile(archivo_csv)
    
    # Escribir datos en el archivo CSV
    with open(archivo_csv, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        if not archivo_existe:
            # Escribir encabezados si el archivo no existe
            escritor.writerow(["Direccion", "Ano Construccion", "Numero Pisos", "Tamano Lote", "Numero Habitaciones", "Numero Banos", "Superficie Construida", "Tipo Construccion", "Estado", "Garaje", "Piscina", "Jardin"])
        # Escribir los datos en una fila separada
        escritor.writerow([direccion, ano_construccion, num_pisos, tam_lote, num_habitaciones, num_banos, superficie, tipo_construccion, estado, garaje, piscina, jardin])
    
    # Mensaje de confirmación
    messagebox.showinfo("Información", "Datos guardados exitosamente!")

def cargar_imagen():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        # Aquí podrías mostrar la imagen o procesarla
        print(f"Imagen cargada: {ruta_imagen}")

def crear_formulario():
    ventana = tk.Tk()
    ventana.title("Formulario de Evaluación de Vivienda")
    
    # Etiquetas y Entradas para los datos
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
    ]
    
    entradas = {}
    for i, texto in enumerate(etiquetas):
        label = tk.Label(ventana, text=texto)
        label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(ventana)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        entradas[texto] = entrada
    
    global entrada_direccion, entrada_ano, entrada_pisos, entrada_lote, entrada_habitaciones, entrada_banos, entrada_superficie, entrada_tipo, entrada_estado
    entrada_direccion = entradas["Dirección:"]
    entrada_ano = entradas["Año de Construcción:"]
    entrada_pisos = entradas["Número de Pisos:"]
    entrada_lote = entradas["Tamaño del Lote (m²):"]
    entrada_habitaciones = entradas["Número de Habitaciones:"]
    entrada_banos = entradas["Número de Baños:"]
    entrada_superficie = entradas["Superficie Construida (m²):"]
    entrada_tipo = entradas["Tipo de Construcción:"]
    entrada_estado = entradas["Estado General:"]
    
    # Casillas de verificación para características adicionales
    global var_garaje, var_piscina, var_jardin
    var_garaje = tk.BooleanVar()
    var_piscina = tk.BooleanVar()
    var_jardin = tk.BooleanVar()
    
    tk.Checkbutton(ventana, text="Garaje", variable=var_garaje).grid(row=len(etiquetas), column=0, columnspan=2, padx=10, pady=5)
    tk.Checkbutton(ventana, text="Piscina", variable=var_piscina).grid(row=len(etiquetas)+1, column=0, columnspan=2, padx=10, pady=5)
    tk.Checkbutton(ventana, text="Jardín", variable=var_jardin).grid(row=len(etiquetas)+2, column=0, columnspan=2, padx=10, pady=5)
    
    # Botón para cargar imágenes
    boton_cargar_imagen = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
    boton_cargar_imagen.grid(row=len(etiquetas)+3, column=0, columnspan=2, pady=10)
    
    # Botón para guardar datos
    boton_guardar = tk.Button(ventana, text="Guardar Datos", command=guardar_datos)
    boton_guardar.grid(row=len(etiquetas)+4, column=0, columnspan=2, pady=10)
    
    ventana.mainloop()

if __name__ == "__main__":
    crear_formulario()
import tensorflow as tf
from tensorflow.keras import layers, models

def crear_modelo():
    # Ejemplo básico de un modelo de red neuronal
    modelo = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    modelo.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return modelo

def entrenar_modelo():
    modelo = crear_modelo()
    
    # Aquí cargarías tus datos de entrenamiento y etiquetas
    # datos_entrenamiento, etiquetas = cargar_datos()
    
    # Ejemplo de entrenamiento
    # modelo.fit(datos_entrenamiento, etiquetas, epochs=5)
    
    modelo.save('models/modelo_entrenado.h5')
    print("Modelo entrenado y guardado.")

if __name__ == "__main__":
    entrenar_modelo()
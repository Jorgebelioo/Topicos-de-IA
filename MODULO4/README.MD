# Requisitos del Sistema

## Descripción

Este proyecto implementa un sistema de reconocimiento facial en tiempo real utilizando DeepFace, OpenCV y FaceNet. El sistema permite identificar estudiantes mediante una cámara web, consultar información académica almacenada en una base de datos SQLite y evaluar el rendimiento del reconocimiento mediante métricas de clasificación.

## Requisitos Previos

* Python 3.10 o superior
* Cámara web
* Sistema operativo Windows, Linux o macOS
* Conexión a Internet para la instalación inicial de dependencias

## Instalación de Dependencias

Instalar las librerías necesarias mediante:

```bash
pip install deepface opencv-python tensorflow pandas numpy scikit-learn albumentations
```

## Librerías Utilizadas

### DeepFace

Biblioteca especializada en reconocimiento facial. Se utiliza para la extracción de características faciales mediante el modelo FaceNet y para realizar la búsqueda de coincidencias dentro de la base de datos de rostros.

### OpenCV (opencv-python)

Biblioteca de visión por computadora utilizada para:

* Captura de video en tiempo real.
* Detección de rostros mediante Haar Cascades.
* Procesamiento y visualización de imágenes.
* Dibujar cuadros y mostrar información en pantalla.

### TensorFlow

Framework de aprendizaje profundo utilizado internamente por DeepFace para ejecutar los modelos de reconocimiento facial.

### Pandas

Biblioteca utilizada por DeepFace para manejar los resultados de búsqueda y comparación de rostros en forma de DataFrames.

### NumPy

Biblioteca fundamental para operaciones numéricas y procesamiento de imágenes.

### Scikit-Learn

Biblioteca utilizada para evaluar el desempeño del sistema mediante las siguientes métricas:

* Accuracy
* Precision
* Recall
* F1-Score
* Classification Report

### Albumentations

Biblioteca utilizada para realizar Data Augmentation y aumentar artificialmente el número de imágenes del conjunto de entrenamiento mediante:

* Volteo horizontal.
* Ajuste de brillo y contraste.
* Rotación.
* Adición de ruido gaussiano.
* Desenfoque.

### SQLite3

Sistema de gestión de bases de datos integrado en Python utilizado para almacenar información de los estudiantes:

* Nombre.
* ID del estudiante.
* Edad.
* Carrera.
* Semestre.

## Modelo Utilizado

El sistema utiliza el modelo:

* FaceNet

Configurado mediante DeepFace con:

* Métrica de distancia: Cosine Similarity.
* Detector facial: OpenCV.
* Reconocimiento en tiempo real mediante búsqueda en base de datos facial.

## Estructura del Proyecto

```text
MODULO4/
│
├── bd/
│   ├── NombrePersona/
│   └── README.md
│
├── test/
│   ├── NombrePersona/
│   └── README.md
│
├── main.py
├── evaluar_modelo.py
├── dataAugmentation.py
└── crear_bd.py

estudiantes.db
```

## Funcionalidades

### Reconocimiento Facial en Tiempo Real

* Captura de video mediante cámara web.
* Detección automática de rostros.
* Identificación de estudiantes registrados.
* Visualización de datos académicos.
* Medición de FPS.
* Medición del tiempo de reconocimiento.

### Evaluación del Modelo

El script `evaluar_modelo.py` permite calcular:

* Accuracy
* Precision
* Recall
* F1-Score
* Reporte de clasificación por clase

### Data Augmentation

El script `dataAugmentation.py` genera imágenes sintéticas para incrementar la variabilidad del conjunto de datos y mejorar la capacidad de generalización del sistema.

## Ejecución

Crear la base de datos:

```bash
python crear_bd.py
```

Generar imágenes aumentadas:

```bash
python dataAugmentation.py
```

Evaluar el modelo:

```bash
python evaluar_modelo.py
```

Iniciar el reconocimiento facial:

```bash
python main.py
```

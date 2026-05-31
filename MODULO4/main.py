import os
import warnings

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

warnings.filterwarnings('ignore')

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import cv2
import time
import sqlite3
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

from deepface import DeepFace

gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        print(f"GPU detectada: {gpus}")

    except RuntimeError:
        pass
else:
    print("No se detectó GPU, usando CPU")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "bd")

DB_PATH = os.path.join(BASE_DIR, "../estudiantes.db")

MODEL_NAME = "Facenet"

if not os.path.exists(DB_PATH):
    print(f"ERROR: No existe la base de datos: {DB_PATH}")
    exit()

conexion = sqlite3.connect(DB_PATH)

cursor = conexion.cursor()

if not os.path.exists(DATABASE_PATH):
    print(f"ERROR: No existe la carpeta: {DATABASE_PATH}")
    exit()

cascade_path = (
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

if not os.path.exists(cascade_path):
    print(f"ERROR: No se encontró: {cascade_path}")
    exit()

face_cascade = cv2.CascadeClassifier(cascade_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Intentando con CAP_DSHOW...")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: No se pudo abrir la cámara")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Sistema iniciado. Presiona 'q' para salir...")

nombre_cache = "Desconocido"

id_cache = ""

edad_cache = ""

semestre_cache = ""

carrera_cache = ""

ultimo_reconocimiento = 0

INTERVALO_RECONOCIMIENTO = 2

prev_time = time.time()

fps = 0

tiempo_reconocimiento = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error leyendo cámara")
        break

    frame = cv2.flip(frame, 1)

    frame_small = cv2.resize(frame, (480, 360))

    gray = cv2.cvtColor(
        frame_small,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        if w <= 0 or h <= 0:
            continue

        cv2.rectangle(
            frame_small,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        ahora = time.time()

        if (
            ahora - ultimo_reconocimiento >
            INTERVALO_RECONOCIMIENTO
        ):

            ultimo_reconocimiento = ahora

            y1 = max(0, y)
            y2 = min(frame_small.shape[0], y + h)

            x1 = max(0, x)
            x2 = min(frame_small.shape[1], x + w)

            rostro = frame_small[
                y1:y2,
                x1:x2
            ]

            if rostro.size == 0:
                continue

            try:

                inicio_reconocimiento = time.time()

                resultado = DeepFace.find(
                    img_path=rostro,
                    db_path=DATABASE_PATH,
                    model_name=MODEL_NAME,
                    distance_metric="cosine",
                    enforce_detection=False,
                    detector_backend="opencv",
                    silent=True
                )

                fin_reconocimiento = time.time()

                tiempo_reconocimiento = (
                    fin_reconocimiento -
                    inicio_reconocimiento
                )

                print(
                    f"Tiempo reconocimiento: "
                    f"{tiempo_reconocimiento:.2f} s"
                )

                nombre_cache = "Desconocido"
                id_cache = ""
                edad_cache = ""
                semestre_cache = ""
                carrera_cache = ""

                if resultado and len(resultado) > 0:

                    df = resultado[0]

                    if df is not None and not df.empty:

                        identity = df.iloc[0]["identity"]

                        nombre_cache = os.path.basename(
                            os.path.dirname(identity)
                        )

                        cursor.execute("""
                        SELECT
                            id_estudiante,
                            edad,
                            carrera,
                            semestre
                        FROM estudiantes
                        WHERE nombre = ?
                        """, (nombre_cache,))

                        datos = cursor.fetchone()

                        if datos:

                            id_cache = str(datos[0])

                            edad_cache = str(datos[1])

                            carrera_cache = datos[2]

                            semestre_cache = str(datos[3])

                        print(
                            f"Reconocido: "
                            f"{nombre_cache}"
                        )

            except Exception as e:

                print(
                    f"Error reconocimiento: {e}"
                )

                nombre_cache = "Desconocido"

                id_cache = ""

                edad_cache = ""

                semestre_cache = ""

                carrera_cache = ""

        cv2.putText(
            frame_small,
            nombre_cache,
            (x, max(0, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        if id_cache:

            cv2.putText(
                frame_small,
                f"ID: {id_cache}",
                (x, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        if edad_cache:

            cv2.putText(
                frame_small,
                f"Edad: {edad_cache}",
                (x, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        if semestre_cache:

            cv2.putText(
                frame_small,
                f"Semestre: {semestre_cache}",
                (x, y + h + 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        if carrera_cache:

            cv2.putText(
                frame_small,
                carrera_cache,
                (x, y + h + 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        frame_small,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame_small,
        f"Reconocimiento: "
        f"{tiempo_reconocimiento:.2f}s",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Reconocimiento Facial",
        frame_small
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

conexion.close()

cv2.destroyAllWindows()

print("Sistema cerrado.")
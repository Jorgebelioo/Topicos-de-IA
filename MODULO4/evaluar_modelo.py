import os

from deepface import DeepFace

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "bd")

TEST_PATH = os.path.join(BASE_DIR, "test")

MODEL_NAME = "Facenet"

y_true = []
y_pred = []

for persona_real in os.listdir(TEST_PATH):

    carpeta_persona = os.path.join(
        TEST_PATH,
        persona_real
    )

    if not os.path.isdir(carpeta_persona):
        continue

    for archivo in os.listdir(carpeta_persona):

        if not archivo.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        ruta_imagen = os.path.join(
            carpeta_persona,
            archivo
        )

        try:

            resultado = DeepFace.find(
                img_path=ruta_imagen,
                db_path=DB_PATH,
                model_name=MODEL_NAME,
                distance_metric="cosine",
                enforce_detection=False,
                detector_backend="opencv",
                silent=True
            )

            prediccion = "Desconocido"

            if (
                resultado and
                len(resultado) > 0 and
                not resultado[0].empty
            ):

                identity = resultado[0].iloc[0]["identity"]

                prediccion = os.path.basename(
                    os.path.dirname(identity)
                )

            y_true.append(persona_real)

            y_pred.append(prediccion)

            print(
                f"Real: {persona_real} "
                f"-> Predicción: {prediccion}"
            )

        except Exception as e:

            print(e)

# métricas

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n===== RESULTADOS =====")

print(f"Accuracy : {accuracy:.4f}")

print(f"Precision: {precision:.4f}")

print(f"Recall   : {recall:.4f}")

print(f"F1 Score : {f1:.4f}")

print("\n===== REPORTE =====")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)
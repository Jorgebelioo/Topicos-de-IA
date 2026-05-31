import cv2
import os
import albumentations as A

# ============================================
# CONFIGURACION
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "bd")

# ============================================
# AUGMENTATIONS
# ============================================

transform = A.Compose([

    A.HorizontalFlip(p=1),

    A.RandomBrightnessContrast(
        brightness_limit=0.2,
        contrast_limit=0.2,
        p=0.8
    ),

    A.Rotate(
        limit=10,
        p=0.7
    ),

    A.GaussNoise(
        p=0.3
    ),

    A.Blur(
        blur_limit=3,
        p=0.2
    )

])

# ============================================
# RECORRER PERSONAS
# ============================================

for persona in os.listdir(DATASET_PATH):

    persona_path = os.path.join(DATASET_PATH, persona)

    if not os.path.isdir(persona_path):
        continue

    print(f"\nProcesando: {persona}")

    for archivo in os.listdir(persona_path):

        if not archivo.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        image_path = os.path.join(persona_path, archivo)

        image = cv2.imread(image_path)

        if image is None:
            continue

        # ============================================
        # GENERAR 5 IMAGENES AUMENTADAS
        # ============================================

        for i in range(5):

            augmented = transform(image=image)

            img_aug = augmented["image"]

            nombre_salida = f"{os.path.splitext(archivo)[0]}_aug_{i}.jpg"

            salida_path = os.path.join(
                persona_path,
                nombre_salida
            )

            cv2.imwrite(salida_path, img_aug)

    print(f"Augmentations completadas para {persona}")

print("\nDATA AUGMENTATION FINALIZADO")
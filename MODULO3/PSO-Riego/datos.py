import os

import pandas as pd

# datos para cargar los datos de sensores
class Datos:
    # lee el archivo CSV y carga los datos en un DataFrame de pandas
    def __init__(self, filepath):
        base = os.path.dirname(os.path.abspath(__file__))
        self.data = pd.read_csv(os.path.join(base, filepath))
    
    def get_datos(self):
        return self.data

    # obtiene los límites de latitud y longitud del conjunto de datos
    def get_lat_lon_limites(self):
        lat_min, lat_max = self.data['Latitud'].min(), self.data['Latitud'].max()
        lon_min, lon_max = self.data['Longitud'].min(), self.data['Longitud'].max()
        return lat_min, lat_max, lon_min, lon_max
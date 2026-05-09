import csv
import numpy as np
from municipio import municipio, establecerMatrizDistancias


def cargarCiudadesDesdeCSV(ruta_csv):
	"""
	Carga ciudades y su matriz de distancias reales desde un CSV.

	El CSV debe tener la primera fila y primera columna con los nombres
	de las ciudades, y el resto ser la matriz de distancias en km.

	Ejemplo de formato:
		,CiudadA,CiudadB,...
		CiudadA,0,303,...
		CiudadB,303,0,...

	ARGUMENTOS:
		ruta_csv: Ruta al archivo CSV con la matriz de distancias

	RETORNA:
		Lista de objetos municipio listos para el algoritmo genético
	"""
	with open(ruta_csv, newline='', encoding='utf-8') as f:
		lector = csv.reader(f)
		filas = list(lector)

	# Primera fila: encabezados (primera celda vacía, luego nombres)
	nombres = filas[0][1:]
	n = len(nombres)

	# Construir matriz de distancias
	matriz = np.zeros((n, n))
	for i, fila in enumerate(filas[1:]):
		for j, valor in enumerate(fila[1:]):
			try:
				matriz[i][j] = float(valor)
			except ValueError:
				matriz[i][j] = 0.0

	# Crear índice nombre → posición
	indiceCiudades = {nombre.strip(): idx for idx, nombre in enumerate(nombres)}

	# Registrar la matriz globalmente en el módulo municipio
	establecerMatrizDistancias(matriz, indiceCiudades)

	# Crear objetos municipio (sin coordenadas reales necesarias)
	ciudades = []
	for nombre in nombres:
		ciudad = municipio(x=0, y=0, nombre=nombre.strip())
		ciudades.append(ciudad)

	print(f"[utils] {n} ciudades cargadas desde '{ruta_csv}'")
	print(f"[utils] Ciudades: {', '.join(nombres)}")
	return ciudades
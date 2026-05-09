import numpy as np

# Matriz global de distancias (en km) entre ciudades
_matrizDistancias = None
_indiceCiudades = {}

def establecerMatrizDistancias(matriz, indices):
	"""
	Establece la matriz de distancias real y el índice de ciudades
	
	ARGUMENTOS:
		matriz: Matriz 2D con distancias en km
		indices: Diccionario {nombre_ciudad: índice_en_matriz}
	"""
	global _matrizDistancias, _indiceCiudades
	_matrizDistancias = matriz
	_indiceCiudades = indices


class municipio:
	"""
	Representa una ciudad con nombre y coordenadas geográficas.
	Usa la matriz de distancias reales si está disponible,
	de lo contrario usa distancia euclidiana.
	
	ARGUMENTOS:
		x: Coordenada X (latitud)
		y: Coordenada Y (longitud)
		nombre: Nombre de la ciudad (requerido para usar matriz real)
	"""
	def __init__(self, x, y, nombre=None):
		self.x = x
		self.y = y
		self.nombre = nombre

	def distancia(self, otro):
		"""
		Calcula la distancia entre dos municipios.
		Prioriza la matriz de distancias reales en km si está disponible.
		
		ARGUMENTOS:
			otro: Objeto municipio destino
		
		RETORNA:
			Distancia en km o euclidiana como fallback
		"""
		global _matrizDistancias, _indiceCiudades

		# Usar matriz de distancias reales si ambas ciudades están indexadas
		if (
			_matrizDistancias is not None
			and self.nombre in _indiceCiudades
			and otro.nombre in _indiceCiudades
		):
			i = _indiceCiudades[self.nombre]
			j = _indiceCiudades[otro.nombre]
			return float(_matrizDistancias[i][j])

		# Fallback: distancia euclidiana
		xDis = abs(self.x - otro.x)
		yDis = abs(self.y - otro.y)
		return np.sqrt((xDis ** 2) + (yDis ** 2))

	def __repr__(self):
		if self.nombre:
			return f"{self.nombre}"
		return f"({self.x}, {self.y})"

	def __eq__(self, otro):
		if isinstance(otro, municipio):
			return self.nombre == otro.nombre
		return False

	def __hash__(self):
		return hash(self.nombre)
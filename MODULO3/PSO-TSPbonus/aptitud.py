class Aptitud:
	"""
	Calcula y almacena la aptitud (fitness) de una ruta.
	La distancia se mide en km usando la matriz de distancias reales.

	ARGUMENTOS:
		ruta: Lista de objetos municipio que representa una ruta completa
	"""
	def __init__(self, ruta):
		self.ruta = ruta
		self.distancia = 0
		self.f_aptitud = 0.0

	def distanciaRuta(self):
		"""
		Calcula la distancia total de la ruta (en km) incluyendo regreso al inicio.

		RETORNA:
			Distancia total de la ruta en km
		"""
		if self.distancia == 0:
			distanciaRelativa = 0
			for i in range(len(self.ruta)):
				puntoInicial = self.ruta[i]
				puntoFinal = self.ruta[i + 1] if i + 1 < len(self.ruta) else self.ruta[0]
				distanciaRelativa += puntoInicial.distancia(puntoFinal)
			self.distancia = distanciaRelativa
		return self.distancia

	def rutaApta(self):
		"""
		Calcula la aptitud de la ruta (inverso de la distancia).
		Mayor fitness = ruta más corta = mejor solución.

		RETORNA:
			Valor de aptitud (fitness)
		"""
		if self.f_aptitud == 0:
			self.f_aptitud = 1 / float(self.distanciaRuta())
		return self.f_aptitud
import numpy as np
import random
from aptitud import Aptitud


def poblacionInicial(tamanoPoblacion, listaCiudades):
	"""
	Genera la población inicial con rutas aleatorias.

	ARGUMENTOS:
		tamanoPoblacion: Número de rutas a generar
		listaCiudades: Lista de objetos municipio

	RETORNA:
		Lista de rutas (cada ruta es una permutación aleatoria de ciudades)
	"""
	poblacion = []
	for _ in range(tamanoPoblacion):
		ruta = random.sample(listaCiudades, len(listaCiudades))
		poblacion.append(ruta)
	return poblacion


def clasificacionRutas(poblacion):
	"""
	Ordena las rutas de mejor (menor distancia) a peor.

	ARGUMENTOS:
		poblacion: Lista de rutas

	RETORNA:
		Lista de tuplas (índice, fitness) ordenada de mayor a menor fitness
	"""
	resultadoFitness = {}
	for i, ruta in enumerate(poblacion):
		resultadoFitness[i] = Aptitud(ruta).rutaApta()

	return sorted(resultadoFitness.items(), key=lambda x: x[1], reverse=True)


def seleccionRutas(popRanked, indivSelecionados):
	"""
	Selecciona índices de rutas mediante selección elitista + ruleta.

	ARGUMENTOS:
		popRanked: Lista ordenada de (índice, fitness)
		indivSelecionados: Número de élite que pasa directamente

	RETORNA:
		Lista de índices seleccionados
	"""
	selectionResults = []
	df = np.array([[item[0], item[1]] for item in popRanked])
	fitness_sum = df[:, 1].sum()
	df_rel = df[:, 1] / fitness_sum * 100
	df_cum = np.cumsum(df_rel)

	# Élite: los mejores pasan directamente
	for i in range(indivSelecionados):
		selectionResults.append(int(popRanked[i][0]))

	# Selección por ruleta para el resto
	for _ in range(len(popRanked) - indivSelecionados):
		pick = 100 * random.random()
		for i in range(len(popRanked)):
			if pick <= df_cum[i]:
				selectionResults.append(int(popRanked[i][0]))
				break

	return selectionResults


def grupoApareamiento(poblacion, selectionResults):
	"""
	Construye el grupo de apareamiento a partir de los índices seleccionados.

	ARGUMENTOS:
		poblacion: Población actual
		selectionResults: Índices seleccionados

	RETORNA:
		Lista de rutas seleccionadas para reproducción
	"""
	grupo = [poblacion[i] for i in selectionResults]
	return grupo
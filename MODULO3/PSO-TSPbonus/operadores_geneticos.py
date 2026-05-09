import random


def reproduccion(progenitor1, progenitor2):
	"""
	Combina dos rutas usando Order Crossover (OX).

	ARGUMENTOS:
		progenitor1: Primera ruta padre
		progenitor2: Segunda ruta padre

	RETORNA:
		Nueva ruta hijo resultado del crossover
	"""
	generacionX = int(random.random() * len(progenitor1))
	generacionY = int(random.random() * len(progenitor2))

	generacionInicial = min(generacionX, generacionY)
	generacionFinal = max(generacionX, generacionY)

	hijoP1 = progenitor1[generacionInicial:generacionFinal]
	hijoP2 = [item for item in progenitor2 if item not in hijoP1]

	return hijoP1 + hijoP2


def reproduccionPoblacion(grupoApareamiento, indivSelecionados):
	"""
	Genera una nueva población mediante reproducción.

	ARGUMENTOS:
		grupoApareamiento: Lista de individuos seleccionados
		indivSelecionados: Número de élite que pasa sin cambios

	RETORNA:
		Lista de nuevas rutas (hijos)
	"""
	hijos = []
	tamano = len(grupoApareamiento) - indivSelecionados
	espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

	# Élite pasa directamente
	for i in range(indivSelecionados):
		hijos.append(grupoApareamiento[i])

	# Cruzar el resto
	for i in range(tamano):
		hijo = reproduccion(espacio[i], espacio[len(grupoApareamiento) - i - 1])
		hijos.append(hijo)

	return hijos


def mutacion(individuo, razonMutacion):
	"""
	Aplica mutación por intercambio (swap) a una ruta.

	ARGUMENTOS:
		individuo: Ruta a mutar
		razonMutacion: Probabilidad de mutación para cada posición

	RETORNA:
		Ruta mutada
	"""
	individuoMutado = individuo.copy()
	for swapped in range(len(individuoMutado)):
		if random.random() < razonMutacion:
			swapWith = int(random.random() * len(individuoMutado))
			individuoMutado[swapped], individuoMutado[swapWith] = (
				individuoMutado[swapWith],
				individuoMutado[swapped],
			)
	return individuoMutado


def mutacionPoblacion(poblacion, razonMutacion):
	"""
	Aplica mutación a toda la población.

	ARGUMENTOS:
		poblacion: Lista de rutas
		razonMutacion: Probabilidad de mutación

	RETORNA:
		Población mutada
	"""
	return [mutacion(ind, razonMutacion) for ind in poblacion]
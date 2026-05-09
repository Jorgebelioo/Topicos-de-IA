from seleccion import poblacionInicial, clasificacionRutas, seleccionRutas, grupoApareamiento
from operadores_geneticos import reproduccionPoblacion, mutacionPoblacion


def nuevaGeneracion(generacionActual, indivSelecionados, razonMutacion):
	"""
	Crea una nueva generación mediante selección, crossover y mutación.

	ARGUMENTOS:
		generacionActual: Población actual de rutas
		indivSelecionados: Número de mejores individuos (élite)
		razonMutacion: Probabilidad de mutación

	RETORNA:
		Nueva población (siguiente generación)
	"""
	popRanked = clasificacionRutas(generacionActual)
	selectionResults = seleccionRutas(popRanked, indivSelecionados)
	grupoApa = grupoApareamiento(generacionActual, selectionResults)
	hijos = reproduccionPoblacion(grupoApa, indivSelecionados)
	nuevaPob = mutacionPoblacion(hijos, razonMutacion)
	return nuevaPob


def algoritmoGenetico(poblacion, tamanoPoblacion, indivSelecionados, razonMutacion, generaciones, verbose=True):
	"""
	Ejecuta el algoritmo genético para el Problema del Viajante (TSP).

	ARGUMENTOS:
		poblacion: Lista de objetos municipio a visitar
		tamanoPoblacion: Número de individuos por generación
		indivSelecionados: Número de élite (pasan sin cambios)
		razonMutacion: Probabilidad de mutación (0.0 - 1.0)
		generaciones: Número de iteraciones del algoritmo
		verbose: Si True, imprime el progreso en consola

	RETORNA:
		Tupla (mejor_ruta, distancia_inicial_km, distancia_final_km)
	"""
	pop = poblacionInicial(tamanoPoblacion, poblacion)
	ranked0 = clasificacionRutas(pop)
	distanciaInicial = 1 / ranked0[0][1]

	if verbose:
		print("=" * 60)
		print("  ALGORITMO GENÉTICO — OPTIMIZACIÓN DE RUTAS (TSP)")
		print("=" * 60)
		print(f"  Ciudades          : {len(poblacion)}")
		print(f"  Tamaño población  : {tamanoPoblacion}")
		print(f"  Élite seleccionada: {indivSelecionados}")
		print(f"  Razón de mutación : {razonMutacion}")
		print(f"  Generaciones      : {generaciones}")
		print("=" * 60)
		print(f"  Distancia inicial : {distanciaInicial:,.2f} km")
		print("-" * 60)

	# Evolución
	for i in range(generaciones):
		pop = nuevaGeneracion(pop, indivSelecionados, razonMutacion)

		if verbose and (i + 1) % 50 == 0:
			dist = 1 / clasificacionRutas(pop)[0][1]
			print(f"  Gen {i+1:4d}/{generaciones}  →  {dist:,.2f} km")

	# Resultado final
	popRankedFinal = clasificacionRutas(pop)
	distanciaFinal = 1 / popRankedFinal[0][1]
	mejorRuta = pop[popRankedFinal[0][0]]

	if verbose:
		mejora = ((distanciaInicial - distanciaFinal) / distanciaInicial) * 100
		print("=" * 60)
		print("  RESULTADOS FINALES")
		print("=" * 60)
		print(f"  Distancia inicial : {distanciaInicial:,.2f} km")
		print(f"  Distancia final   : {distanciaFinal:,.2f} km")
		print(f"  Mejora total      : {mejora:.2f}%")
		print(f"  Reducción         : {distanciaInicial - distanciaFinal:,.2f} km")
		print("=" * 60)

	return mejorRuta, distanciaInicial, distanciaFinal
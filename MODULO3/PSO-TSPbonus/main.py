import os
from utils import cargarCiudadesDesdeCSV
from algoritmo_genetico import algoritmoGenetico
from generador_reportes import GeneradorReportes

if __name__ == "__main__":

	
	ruta_csv = os.path.join(os.path.dirname(__file__), 'ciudades.csv')
	ciudades = cargarCiudadesDesdeCSV(ruta_csv)

	# Ejecutar el algoritmo genético
	mejorRuta, distancia_inicial, distancia_final = algoritmoGenetico(
		poblacion=ciudades,
		tamanoPoblacion=100,
		indivSelecionados=20,
		razonMutacion=0.01,
		generaciones=500,
		verbose=True
	)

	# Mostrar resultados en consola
	print("\nMEJOR RUTA ENCONTRADA:")
	print("-" * 60)
	for idx, ciudad in enumerate(mejorRuta, 1):
		print(f"  {idx:2d}. {ciudad}")
	print(f"  {len(mejorRuta)+1:2d}. {mejorRuta[0]} (regreso al inicio)")
	print("-" * 60)

	# Mostrar ruta con flechas
	print("\nRUTA OPTIMIZADA:")
	nombres = [str(c) for c in mejorRuta]
	ruta_texto = " -> ".join(nombres) + f" -> {nombres[0]}"
	print(ruta_texto)

	# Generar reporte en TXT
	print("\n" + "=" * 60)
	print("GENERANDO REPORTE...")

	generador = GeneradorReportes()
	archivo_reporte = generador.crear_reporte(mejorRuta, distancia_inicial, distancia_final)

	print(f"Reporte generado: {archivo_reporte}")
	print("=" * 60)
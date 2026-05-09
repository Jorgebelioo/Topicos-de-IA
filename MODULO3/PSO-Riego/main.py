import time
from datos import Datos
from optimizador_sensores import OptimizadorSensores
from visualizar import Visualizar

if __name__ == "__main__":
    
    datocsv = Datos("datos/cultivos.csv")
    data = datocsv.get_datos()

    
    optimizador = OptimizadorSensores(data, n_sensores=5)
    mejor_costo, mejor_posicion = optimizador.optimizar(iters=30)
    mejores_posiciones = optimizador.get_mejores_posiciones()

    # Muestra de Resultados obtenidos
    print("--------------------------------------------------------")
    print(f"Mejor Costo: {mejor_costo:.2f}")
    print("Mejores posiciones para sensores (Latitud, Longitud):")
    for i, (lat, lon) in enumerate(mejores_posiciones, start=1):
        print(f"Sensor {i}: Latitud={lat:.6f}, Longitud={lon:.6f}")

    # Grafica de los sensores y cultivos
    visualizar = Visualizar()
    visualizar.mostrar(data, mejores_posiciones)


#    print("\nRobustez del algoritmo PSO:")
#costos = []
#for _ in range(10):
#    costo, _ = optimizador.optimizar(iters=10)
#    costos.append(costo)

#print(f"  Repeticiones: {len(costos)}")
#print(f"  Media:        {sum(costos)/len(costos):.4f}")
#print(f"  Mejor:        {min(costos):.4f}")
#print(f"  Peor:         {max(costos):.4f}")
#print(f"  Desv. Est.:   {(sum((x - sum(costos)/len(costos))**2 for x in costos)/len(costos))**0.5:.4f}")

print("\nResumen:")
tiempos = []
for _ in range(5):
    inicio = time.time()
    optimizador.optimizar(iters=100)
    tiempos.append(round(time.time() - inicio, 4))

print(f"Tiempos (s): {tiempos}")
print(f"Min: {min(tiempos):.4f}  Max: {max(tiempos):.4f}  Promedio: {sum(tiempos)/len(tiempos):.4f}")
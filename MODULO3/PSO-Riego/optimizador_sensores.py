import numpy as np
import pyswarms as ps

class OptimizadorSensores:
    # Prepara las variables para la optimización de la distribución de sensores
    def __init__(self, data, n_sensores):
        self.data = data
        self.n_sensores = n_sensores
        self.n_dim = n_sensores * 2
        self.lat_min, self.lat_max, self.lon_min, self.lon_max = self._get_bounds()
        self.options = {'c1': 0.3, 'c2': 0.6, 'w': 0.5}
        self.best_cost = None
        self.best_pos = None

    # Obtiene los límites de latitud y longitud del conjunto de datos
    def _get_bounds(self):
        lat_min = self.data['Latitud'].min()
        lat_max = self.data['Latitud'].max()
        lon_min = self.data['Longitud'].min()
        lon_max = self.data['Longitud'].max()
        return lat_min, lat_max, lon_min, lon_max
    
    def funcion_fitness(self, posiciones):
        
        coverage_radius = 0.025 # El coverage radius significa que es el radio que esta alrededor de cada 
                                #sensor dentro del cual los puntos del dataset de cultivos se consideran vecinos.
        total_var = 0 # total de la varianza
        penalizacion_redundancia = 0 

        # Recorremos los datos de latitud y longitud de posiciones
        for lat, lon in posiciones: 
            #Calcula la distancia euclidiana entre el sensor(lat, lon) y cada punto del dataset
            # d = √((x2 - x1)² + (y2 - y1)²)
            distances = np.sqrt(
                (self.data['Latitud'] - lat) ** 2 +
                (self.data['Longitud'] - lon) ** 2
            )
            #Filtra solo los puntos cuya distancia al sensor es menor que coverage_radius
            neighbors = self.data[distances < coverage_radius]
            #Si hay suficientes puntos (más de 3) calcula la varianza de cada una de las cuatro variables 
            #y luego hace el promedio de esas varianzas. 
            # local_var = qué tanto cambian Humedad, Salinidad, Temperatura y Elevacion cerca del sensor
            if len(neighbors) > 3:
                local_var = neighbors[['Humedad', 'Salinidad', 'Temperatura', 'Elevacion']].var().mean()
            else:
            # Penalización si hay 3 o menos puntos 
                local_var = 10
            #Se van sumando las varianzas locales al total varianza
            total_var += local_var

        # Penalización por sensores cercanos
        # aqui se toma la distancia euclidiana entre cada par de sensores
        # para verificar que si su distancia es menor a la separacion_minima 
        # aplicar penalizacion.
        separacion_minima = 0.005      # distancia mínima aceptable entre dos sensores en grados
        peso_redundante = 100.0        # peso de la penalización
        
        for i in range(len(posiciones)):
            for j in range(i + 1, len(posiciones)):
                d = np.linalg.norm(np.array(posiciones[i]) - np.array(posiciones[j]))
                if d < separacion_minima:
                    penalizacion_redundancia += (separacion_minima - d) * peso_redundante

        # Calculamos y devolvemos el valor fitness
        fitness_value = total_var + penalizacion_redundancia
        return fitness_value

    # Aplica funcion_fitness a cada partícula del enjambre 
    # y devuelve un array con sus valores de fitness.

    def funcion_objetivo(self, x):
        results = []
        for particula in x:  
            posiciones = particula.reshape((self.n_sensores, 2))
            results.append(self.funcion_fitness(posiciones))
        return np.array(results)
    
    # Realiza la optimización usando Pyswarms con el método GlobalBestPSO
    # Retorna el mejor costo y las mejores posiciones de los sensores 
    def optimizar(self, iters):
        optimizador = ps.single.GlobalBestPSO(
            n_particles=50,
            dimensions=self.n_dim,
            options=self.options,
            bounds=(np.array([self.lat_min, self.lon_min]*self.n_sensores),
                    np.array([self.lat_max, self.lon_max]*self.n_sensores))
        )
        self.mejor_costo, self.mejores_posiciones = optimizador.optimize(self.funcion_objetivo, iters=iters)
        return self.mejor_costo, self.mejores_posiciones

    # Obtiene las mejores posiciones de los sensores
    def get_mejores_posiciones(self):
        if self.mejores_posiciones is not None:
            return self.mejores_posiciones.reshape((self.n_sensores, 2))
        return None

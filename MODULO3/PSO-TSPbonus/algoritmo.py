import random

n = 20

class Particula:
    def __init__(self, num_ciudades):
        self.num_ciudades = num_ciudades
        perm = list(range(1, num_ciudades + 1))
        random.shuffle(perm)
        self.posicion = [0] + perm + [0]
        self.velocidad = []
        self.mejor_posicion = self.posicion[:]
        self.mejor_fitness = float('inf')

    def evaluar_fitness(self, matriz):
        distancia_total = 0
        for i in range(1, len(self.posicion)):
            distancia_total += matriz[self.posicion[i - 1]][self.posicion[i]]
        if distancia_total < self.mejor_fitness:
            self.mejor_posicion = self.posicion[:]
            self.mejor_fitness = distancia_total
        return distancia_total

    def actualizar_velocidad(self, gbest_fitness, gbest_posicion, w=0.3, c1=0.6, c2=1):
        nueva_velocidad = []
        indices_visitados = set()

        if gbest_fitness == float('inf') or random.random() > 0.85:
            self.velocidad = 'Reshuffle'
            return

        for i in range(1, self.num_ciudades):
            if random.random() < w:
                indices_visitados.add(i)
                continue
            elif random.random() < c1:
                swap_idx = self.mejor_posicion.index(self.posicion[i])
                if i not in indices_visitados and swap_idx not in indices_visitados:
                    nueva_velocidad.append((i, swap_idx))
                    indices_visitados.add(i)
                    indices_visitados.add(swap_idx)
            elif random.random() < c2:
                swap_idx = gbest_posicion.index(self.posicion[i])
                if i not in indices_visitados and swap_idx not in indices_visitados:
                    nueva_velocidad.append((i, swap_idx))
                    indices_visitados.add(i)
                    indices_visitados.add(swap_idx)

        self.velocidad = nueva_velocidad

    def actualizar_posicion(self):
        if self.velocidad == 'Reshuffle':
            i, j = random.sample(range(1, self.num_ciudades + 1), 2)
            self.posicion[i], self.posicion[j] = self.posicion[j], self.posicion[i]
        else:
            for i, j in self.velocidad:
                self.posicion[i], self.posicion[j] = self.posicion[j], self.posicion[i]


def pso_tsp(num_ciudades, matriz, num_particulas=(4*n)**2, max_iter=250, w=0.3, c1=0.6, c2=1.0, verbosidad=10):
    particulas = [Particula(num_ciudades) for _ in range(num_particulas)]
    historial = []
    gbest_posicion = None
    gbest_fitness = float('inf')

    for it in range(max_iter):
        for p in particulas:
            fitness = p.evaluar_fitness(matriz)
            if fitness < p.mejor_fitness:
                p.mejor_fitness = fitness
                p.mejor_posicion = p.posicion[:]
            if fitness < gbest_fitness:
                gbest_fitness = fitness
                gbest_posicion = p.posicion[:]

        historial.append(gbest_fitness)

        for p in particulas:
            p.actualizar_velocidad(gbest_fitness, gbest_posicion, w, c1, c2)
            p.actualizar_posicion()

        if it % verbosidad == 0:
            print('-' * 30)
            print(f'Iteracion: {it + 1}')
            print(f'Mejor distancia: {gbest_fitness}')
            print('-' * 30)

        if len(historial) >= 50 and len(set(historial[-25:])) == 1:
            print("Convergencia alcanzada, deteniendo...")
            break

    return gbest_posicion, gbest_fitness, historial
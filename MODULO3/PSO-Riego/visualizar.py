import matplotlib.pyplot as plt
class Visualizar:
    def mostrar(self, data, mejores_posiciones):
        plt.figure(figsize=(8,6))
        # Colores para cada cultivo
        cultivos = {
            'Maiz': 'gold',
            'Tomate': 'red',
            'Chile': 'green'
        }
        # Graficar cada cultivo con su color
        for cultivo, color in cultivos.items():
            subset = data[data['Cultivo'] == cultivo]
            plt.scatter(subset['Longitud'], subset['Latitud'],
                        color=color, s=40, label=cultivo, alpha=0.7)

        # Graficar las mejores posiciones de los sensores
        plt.scatter(mejores_posiciones[:,1], mejores_posiciones[:,0], color='black', s=120, marker='x', label='Sensores óptimos')
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.title("Ubicaciones Optimas de Sensores en Cultivos")
        plt.legend()
        plt.show()
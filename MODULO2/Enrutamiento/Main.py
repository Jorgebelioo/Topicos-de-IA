import os
import matplotlib.pyplot as plt
from RecocidoSimulado import RecocidoSimulado
from DatosRutas import DatosRutas


class SimuladorRutas:
    def __init__(self, ruta_distancias, ruta_combustible, ruta_ubicaciones, num_vehiculos=10):
        # Rutas absolutas (evita errores de path)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.datos = DatosRutas(
            os.path.join(base_dir, ruta_distancias),
            os.path.join(base_dir, ruta_combustible),
            os.path.join(base_dir, ruta_ubicaciones)
        )

        self.num_vehiculos = num_vehiculos
        self.centros = list(range(1, num_vehiculos + 1))
        self.rutas_iniciales = None
        self.recocido = None
        self.resultado_rutas = None
        self.costo_final = None

    def ejecutar(self):
        """Carga datos, ejecuta optimización y grafica."""
        self.datos.cargar()

        self.rutas_iniciales = self.datos.inicializar_rutas(
            self.num_vehiculos, self.centros
        )

        self.recocido = RecocidoSimulado(
            self.datos.matriz_distancias,
            self.datos.matriz_combustible,
            self.rutas_iniciales
        )

        self.resultado_rutas, self.costo_final = self.recocido.recocidoSimulado()

        self.mostrar_resultados()
        self.graficar_rutas()  #grafica 

    def mostrar_resultados(self):
        """Imprime las rutas optimizadas."""
        print("\n=== RESULTADOS FINALES ===\n")
        print(f"Costo total óptimo: {self.costo_final:,.2f}\n")

        for i, ruta in enumerate(self.resultado_rutas, 1):
            nombres = [self.datos.mapa_nombres[idx] for idx in ruta]
            print(f"Ruta {i:02d} -> {' -> '.join(nombres)}\n")

    def graficar_rutas(self):
        """Grafica las rutas optimizadas."""
        coords = self.datos.ubicaciones

        plt.figure()

        # Dibujar rutas
        for i, ruta in enumerate(self.resultado_rutas):
            x = []
            y = []

            for idx in ruta:
                fila = coords.iloc[idx - 1]
                x.append(fila["Longitud_WGS84"])
                y.append(fila["Latitud_WGS84"])

            plt.plot(x, y, marker='o', label=f'Ruta {i+1}')

        # Separar centros y tiendas
        if "Tipo" in coords.columns:
            centros = coords[coords["Tipo"] == "Centro"]
            tiendas = coords[coords["Tipo"] != "Centro"]

            plt.scatter(
                centros["Longitud_WGS84"],
                centros["Latitud_WGS84"],
                marker='s',
                s=100,
                label="Centros"
            )

            plt.scatter(
                tiendas["Longitud_WGS84"],
                tiendas["Latitud_WGS84"],
                marker='o',
                label="Tiendas"
            )
        else:
            # Si no hay columna Tipo
            plt.scatter(
                coords["Longitud_WGS84"],
                coords["Latitud_WGS84"]
            )

        # Etiquetas
        for i, fila in coords.iterrows():
            plt.text(
                fila["Longitud_WGS84"],
                fila["Latitud_WGS84"],
                fila["Nombre"],
                fontsize=8
            )

        plt.title("Rutas optimizadas")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.legend()
        plt.grid()

        plt.show()


if __name__ == "__main__":
    simulador = SimuladorRutas(
        ruta_distancias="data/matriz_distancias.csv",
        ruta_combustible="data/matriz_costos_combustible.csv",
        ruta_ubicaciones="data/datos_distribucion_tiendas.csv",
        num_vehiculos=10
    )

    simulador.ejecutar()
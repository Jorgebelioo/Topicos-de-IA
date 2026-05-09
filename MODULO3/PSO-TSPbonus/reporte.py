class Reporte:

    def __init__(self, ciudades):
        self.ciudades = ciudades

    def mostrar(self, ruta, distancia, historial):
        print("\n" + "=" * 50)
        print("  RESULTADO FINAL")
        print("=" * 50)
        mejora = historial[0] - distancia
        print(f"  Distancia total  : {distancia:.0f} km")
        print(f"  Mejora obtenida  : {mejora:.0f} km ({mejora / historial[0] * 100:.1f}%)")
        print("\n  Orden de visita:")
        for i, idx in enumerate(ruta[1:-1], 1):
            print(f"    {i:2d}. {self.ciudades[idx - 1]}")
        print(f"    --> Regreso a {self.ciudades[ruta[1] - 1]}")
        nombres = [self.ciudades[idx - 1] for idx in ruta[1:-1]]
        print("\n  Ruta completa:")
        print(f"    {' -> '.join(nombres)} -> {self.ciudades[ruta[1] - 1]}")
        print("=" * 50)
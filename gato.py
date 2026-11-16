from animal import Animal
from gestor_razas import GestorRazas


class Gato(Animal):
    def __init__(self, nombre, peso, edad, raza="Genérico"):
        super().__init__(nombre, peso, edad)
        self.raza = raza

    def tipo_animal(self):
        return "gato"

    def get_raza(self):
        return self.raza

    def rango_ideal(self):
        gestor = GestorRazas()
        rangos = gestor.obtener_datos_raza(self.tipo_animal(), self.get_raza())

        if rangos:
            return rangos

        # Valores por defecto en caso de que la raza se haya borrado o no exista
        return {"t_min": 18, "t_max": 30, "h_min": 30, "h_max": 60}
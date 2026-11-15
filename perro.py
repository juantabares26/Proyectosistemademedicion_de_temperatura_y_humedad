from animal import Animal
from gestor_razas import GestorRazas

class Perro(Animal):
    def __init__(self, nombre, peso, edad, raza="Criollo"):
        super().__init__(nombre, peso, edad, raza)

    def tipo_animal(self):
        return "perro"

    def rango_ideal(self):
        gestor = GestorRazas()
        rangos = gestor.obtener_rango_raza(self.tipo_animal(), self.get_raza())

        # Red de seguridad: si no encuentra la raza en el Excel, devuelve el Genérico
        if rangos is None:
            return gestor.obtener_rango_raza(self.tipo_animal(), "Criollo")

        return rangos
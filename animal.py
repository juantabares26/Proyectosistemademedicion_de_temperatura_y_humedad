class Animal:
    def __init__(self, nombre, peso, edad, raza="Genérico"):
        self.__nombre = nombre
        self.__peso = peso
        self.__edad = edad
        self.__raza = raza

        self.set_nombre(nombre)
        self.set_peso(peso)
        self.set_edad(edad)
        self.set_raza(raza)

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre.strip()

    def get_raza(self):
        return self.__raza

    def set_raza(self, raza):
        if not isinstance(raza, str) or not raza.strip():
            raise ValueError("La raza no puede estar vacía.")
        self.__raza = raza.strip()

    def get_peso(self):
        return self.__peso

    def set_peso(self, peso):
        if not isinstance(peso, (int, float)) or isinstance(peso, bool) or peso <= 0:
            raise ValueError("El peso debe ser mayor que cero.")
        self.__peso = float(peso)

    def get_edad(self):
        return self.__edad

    def set_edad(self, edad):
        if not isinstance(edad, int) or isinstance(edad, bool) or edad < 0:
            raise ValueError("La edad debe ser un entero no negativo.")
        self.__edad = edad

    def tipo_animal(self):
        raise NotImplementedError("El método debe implementarse en una clase hija.")

    def rango_ideal(self):
        raise NotImplementedError("El método debe implementarse en una clase hija.")

    def obtener_datos(self):
        return {
            "tipo": self.tipo_animal(),
            "raza": self.__raza,
            "nombre": self.__nombre,
            "peso": self.__peso,
            "edad": self.__edad
        }
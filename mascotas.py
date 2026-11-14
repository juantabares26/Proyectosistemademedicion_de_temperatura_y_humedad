import json
import os


class GestorMascotas:
    def __init__(self, archivo="mascotas.json"):
        self.__archivo = archivo
        self.__mascotas = self.cargar_mascotas()

    def cargar_mascotas(self):
        if not os.path.exists(self.__archivo):
            return []

        try:
            with open(self.__archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError("El archivo de mascotas tiene un formato incorrecto.")

            return datos

        except json.JSONDecodeError as error:
            raise ValueError("El archivo JSON está dañado.") from error

    def guardar_mascotas(self):
        with open(self.__archivo, "w", encoding="utf-8") as archivo:
            json.dump(
                self.__mascotas,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    def buscar_por_nombre(self, nombre, tipo=None):
        for mascota in self.__mascotas:
            if mascota["nombre"].casefold() == nombre.casefold():
                if tipo is None or mascota["tipo"] == tipo:
                    return mascota

        return None

    def registrar_mascota(self, animal):
        if self.buscar_por_nombre(
                animal.get_nombre(),
                animal.tipo_animal()
        ) is not None:
            raise ValueError(
                "Ya existe una mascota de esa especie con ese nombre."
            )

        self.__mascotas.append(animal.obtener_datos())
        self.guardar_mascotas()

    def listar_mascotas(self):
        return self.__mascotas.copy()
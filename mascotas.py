import json
import os

class GestorMascotas:
    def __init__(self, archivo="mascotas.json"):
        self.archivo = archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

    def listar_mascotas(self):
        with open(self.archivo, "r") as f:
            return json.load(f)

    def buscar_por_nombre(self, nombre, especie=None):
        for m in self.listar_mascotas():
            if m["nombre"] == nombre:
                if especie and m["tipo"] != especie:
                    continue
                return m
        return None

    def registrar_mascota(self, mascota):
        datos = self.listar_mascotas()
        datos.append(mascota.obtener_datos())
        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)

    def actualizar_mascota(self, nombre, nuevo_peso, nueva_edad):
        """Busca una mascota por nombre, actualiza su peso y edad, y guarda los cambios."""
        datos = self.listar_mascotas()
        for m in datos:
            if m["nombre"] == nombre:
                m["peso"] = nuevo_peso
                m["edad"] = nueva_edad
                break
        with open(self.archivo, "w") as f:
            json.dump(datos, f, indent=4)
from mascotas import GestorMascotas
from gestor_razas import GestorRazas
from perro import Perro
from gato import Gato
from sensorAmbiente import SensorAmbiental
from evaluacionAmbiente import EvaluadorAmbiente


class ControladorAplicacion:
    def __init__(self):
        self.gestor_mascotas = GestorMascotas()
        self.gestor_razas = GestorRazas()
        self.sensor = SensorAmbiental()
        self.evaluador = EvaluadorAmbiente()

    def obtener_lista_razas(self, especie):
        return self.gestor_razas.obtener_razas(especie)

    def obtener_lista_mascotas(self):
        mascotas = self.gestor_mascotas.listar_mascotas()
        return [f"{m['nombre']} - {m['tipo']}" for m in mascotas]

    def verificar_nombre_existente(self, nombre, especie):
        return self.gestor_mascotas.buscar_por_nombre(nombre, especie) is not None

    def registrar_mascota(self, especie, nombre, peso, edad, raza, apellido=""):
        nombre_completo = nombre.strip()
        if apellido.strip():
            nombre_completo = f"{nombre_completo} {apellido.strip()}"

        if self.verificar_nombre_existente(nombre_completo, especie):
            raise ValueError(f"El nombre '{nombre_completo}' ya existe. Intenta con otro apellido.")

        if especie == "perro":
            nuevo_animal = Perro(nombre_completo, peso, edad, raza)
        elif especie == "gato":
            nuevo_animal = Gato(nombre_completo, peso, edad, raza)
        else:
            raise ValueError("Especie no válida.")

        self.gestor_mascotas.registrar_mascota(nuevo_animal)

    def registrar_raza(self, especie, raza, t_min, t_max, h_min, h_max):
        self.gestor_razas.agregar_raza(especie, raza, t_min, t_max, h_min, h_max)

    def actualizar_datos_mascota(self, nombre_formateado, peso, edad):
        nombre = nombre_formateado.rsplit(" - ", 1)[0]
        self.gestor_mascotas.actualizar_mascota(nombre, peso, edad)

    def simular_monitoreo(self, nombre_formateado):
        nombre = nombre_formateado.rsplit(" - ", 1)[0]
        datos = self.gestor_mascotas.buscar_por_nombre(nombre)
        if not datos:
            raise ValueError("Mascota no encontrada en el sistema.")

        if datos["tipo"] == "perro":
            animal = Perro(datos["nombre"], datos["peso"], datos["edad"], datos.get("raza", "Genérico"))
        else:
            animal = Gato(datos["nombre"], datos["peso"], datos["edad"], datos.get("raza", "Genérico"))

        mediciones = self.sensor.leer_mediciones()
        evaluacion = self.evaluador.evaluar_ambiente(animal, mediciones)
        return mediciones, evaluacion

    def obtener_datos_raza(self, especie, raza):
        return self.gestor_razas.obtener_datos_raza(especie, raza)

    def modificar_raza(self, especie, raza_antigua, nuevo_nombre_raza, t_min, t_max, h_min, h_max):
        self.gestor_razas.actualizar_raza(especie, raza_antigua, nuevo_nombre_raza, t_min, t_max, h_min, h_max)

    def eliminar_raza(self, especie, raza):
        self.gestor_razas.eliminar_raza(especie, raza)
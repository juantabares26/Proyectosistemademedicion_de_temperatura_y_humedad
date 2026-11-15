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
        # Devuelve solo los nombres para llenar el menú desplegable
        mascotas = self.gestor_mascotas.listar_mascotas()
        return [m["nombre"] for m in mascotas]

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

    def simular_monitoreo(self, nombre_mascota):
        """Simula una lectura y la evalúa contra los parámetros de la mascota."""
        # 1. Buscar los datos en el JSON
        datos = self.gestor_mascotas.buscar_por_nombre(nombre_mascota)
        if not datos:
            raise ValueError("Mascota no encontrada en el sistema.")

        # 2. Reconstruir el objeto para tener acceso a sus rangos
        if datos["tipo"] == "perro":
            animal = Perro(datos["nombre"], datos["peso"], datos["edad"], datos.get("raza", "Genérico"))
        else:
            animal = Gato(datos["nombre"], datos["peso"], datos["edad"], datos.get("raza", "Genérico"))

        # 3. Simular clima y evaluar
        mediciones = self.sensor.leer_mediciones()
        evaluacion = self.evaluador.evaluar_ambiente(animal, mediciones)

        return mediciones, evaluacion
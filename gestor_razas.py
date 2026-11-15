import os
from openpyxl import Workbook, load_workbook


class GestorRazas:
    def __init__(self, archivo="parametros_razas.xlsx"):
        self.archivo = archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea el archivo Excel con sus hojas y encabezados si no existe."""
        if not os.path.exists(self.archivo):
            wb = Workbook()

            # Crear hoja para Perros
            ws_perros = wb.active
            ws_perros.title = "perro"
            ws_perros.append(["Raza", "Temp_Min", "Temp_Max", "Humedad_Min", "Humedad_Max"])

            # Crear hoja para Gatos
            ws_gatos = wb.create_sheet(title="gato")
            ws_gatos.append(["Raza", "Temp_Min", "Temp_Max", "Humedad_Min", "Humedad_Max"])

            # Añadimos una raza "Genérica" por defecto para que no esté vacío
            ws_perros.append(["Criollo", 18, 26, 30, 70])
            ws_gatos.append(["Criollo", 20, 26, 30, 70])

            wb.save(self.archivo)

    def obtener_razas(self, especie):
        """Devuelve una lista con los nombres de las razas registradas para una especie."""
        especie = especie.lower()
        wb = load_workbook(self.archivo, read_only=True)

        if especie not in wb.sheetnames:
            return []

        ws = wb[especie]
        razas = []

        # Leer desde la fila 2 (evitando encabezados)
        for fila in ws.iter_rows(min_row=2, values_only=True):
            if fila[0]:  # Si la celda de la raza tiene texto
                razas.append(fila[0])

        wb.close()
        return razas

    def obtener_rango_raza(self, especie, raza):
        """Devuelve un diccionario con los rangos de temp y humedad de una raza."""
        especie = especie.lower()
        wb = load_workbook(self.archivo, read_only=True)

        if especie not in wb.sheetnames:
            return None

        ws = wb[especie]
        for fila in ws.iter_rows(min_row=2, values_only=True):
            # Comparamos ignorando mayúsculas y minúsculas
            if fila[0] and fila[0].casefold() == raza.casefold():
                rango = {
                    "temperatura": (fila[1], fila[2]),
                    "humedad": (fila[3], fila[4])
                }
                wb.close()
                return rango

        wb.close()
        return None  # Si no encuentra la raza

    def agregar_raza(self, especie, raza, temp_min, temp_max, hum_min, hum_max):
        """Agrega una nueva raza y sus parámetros a la hoja correspondiente."""
        especie = especie.lower()

        # Abrimos el archivo en modo escritura (sin read_only)
        wb = load_workbook(self.archivo)

        if especie not in wb.sheetnames:
            wb.close()
            raise ValueError("Especie no válida. Debe ser 'perro' o 'gato'.")

        ws = wb[especie]

        # Verificar si la raza ya existe para no duplicarla
        for fila in ws.iter_rows(min_row=2, values_only=True):
            if fila[0] and fila[0].casefold() == raza.casefold():
                wb.close()
                raise ValueError("Esta raza ya está registrada en el sistema.")

        # Agregar la nueva fila al final
        ws.append([raza, float(temp_min), float(temp_max), float(hum_min), float(hum_max)])
        wb.save(self.archivo)
        wb.close()
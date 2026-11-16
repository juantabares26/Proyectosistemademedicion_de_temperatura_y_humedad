import openpyxl
import os


class GestorRazas:
    def __init__(self, archivo="razas.xlsx"):
        self.archivo = archivo
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        if not os.path.exists(self.archivo):
            wb = openpyxl.Workbook()
            ws_perros = wb.active
            ws_perros.title = "perro"
            ws_perros.append(["Raza", "T_Min", "T_Max", "H_Min", "H_Max"])

            ws_gatos = wb.create_sheet(title="gato")
            ws_gatos.append(["Raza", "T_Min", "T_Max", "H_Min", "H_Max"])

            wb.save(self.archivo)

    def agregar_raza(self, especie, raza, t_min, t_max, h_min, h_max):
        wb = openpyxl.load_workbook(self.archivo)
        ws = wb[especie]
        ws.append([raza, float(t_min), float(t_max), float(h_min), float(h_max)])
        wb.save(self.archivo)

    def obtener_razas(self, especie):
        wb = openpyxl.load_workbook(self.archivo)
        ws = wb[especie]
        return [row[0] for row in ws.iter_rows(min_row=2, values_only=True) if row[0] is not None]

    def obtener_datos_raza(self, especie, raza):
        wb = openpyxl.load_workbook(self.archivo)
        ws = wb[especie]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] == raza:
                return {"t_min": row[1], "t_max": row[2], "h_min": row[3], "h_max": row[4]}
        return None

    def actualizar_raza(self, especie, raza_antigua, nuevo_nombre_raza, t_min, t_max, h_min, h_max):
        wb = openpyxl.load_workbook(self.archivo)
        ws = wb[especie]
        for fila in ws.iter_rows(min_row=2):
            if fila[0].value == raza_antigua:
                fila[0].value = nuevo_nombre_raza
                fila[1].value = float(t_min)
                fila[2].value = float(t_max)
                fila[3].value = float(h_min)
                fila[4].value = float(h_max)
                break
        wb.save(self.archivo)

    def eliminar_raza(self, especie, raza):
        """Busca la fila correspondiente a la raza y la elimina permanentemente del Excel."""
        wb = openpyxl.load_workbook(self.archivo)
        ws = wb[especie]
        fila_a_eliminar = None

        for row in range(2, ws.max_row + 1):
            if ws.cell(row=row, column=1).value == raza:
                fila_a_eliminar = row
                break

        if fila_a_eliminar:
            ws.delete_rows(fila_a_eliminar, 1)  # Borra 1 fila a partir del índice encontrado
            wb.save(self.archivo)
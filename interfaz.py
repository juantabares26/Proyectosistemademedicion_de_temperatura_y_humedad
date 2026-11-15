import tkinter as tk
from tkinter import ttk, messagebox
from controlador import ControladorAplicacion


class VentanaConfiguracion(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador
        self.title("Administración de Razas")
        self.geometry("300x350")
        self.grab_set()

        ttk.Label(self, text="Especie:").pack(pady=5)
        self.combo_especie = ttk.Combobox(self, values=["perro", "gato"], state="readonly")
        self.combo_especie.pack()
        self.combo_especie.current(0)

        ttk.Label(self, text="Nombre de la Raza:").pack(pady=5)
        self.entry_raza = ttk.Entry(self)
        self.entry_raza.pack()

        ttk.Label(self, text="Temp Mínima y Máxima (°C):").pack(pady=5)
        frame_temp = ttk.Frame(self)
        frame_temp.pack()
        self.entry_tmin = ttk.Entry(frame_temp, width=7)
        self.entry_tmin.pack(side=tk.LEFT, padx=5)
        self.entry_tmax = ttk.Entry(frame_temp, width=7)
        self.entry_tmax.pack(side=tk.LEFT, padx=5)

        ttk.Label(self, text="Humedad Mín y Máx (%):").pack(pady=5)
        frame_hum = ttk.Frame(self)
        frame_hum.pack()
        self.entry_hmin = ttk.Entry(frame_hum, width=7)
        self.entry_hmin.pack(side=tk.LEFT, padx=5)
        self.entry_hmax = ttk.Entry(frame_hum, width=7)
        self.entry_hmax.pack(side=tk.LEFT, padx=5)

        ttk.Button(self, text="Guardar Raza", command=self.guardar_raza).pack(pady=20)

    def guardar_raza(self):
        try:
            self.controlador.registrar_raza(
                self.combo_especie.get(), self.entry_raza.get(),
                self.entry_tmin.get(), self.entry_tmax.get(),
                self.entry_hmin.get(), self.entry_hmax.get()
            )
            messagebox.showinfo("Éxito", "Raza guardada.")
            self.parent.actualizar_razas()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class VentanaModificarMascota(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador
        self.title("Modificar Mascota")
        self.geometry("300x250")
        self.grab_set()

        ttk.Label(self, text="Seleccionar Mascota:").pack(pady=10)
        self.combo_mascotas = ttk.Combobox(self, state="readonly", width=25)
        self.combo_mascotas.pack(pady=5)

        self.combo_mascotas.bind("<<ComboboxSelected>>", self.limpiar_casillas)

        ttk.Label(self, text="Nuevo Peso (kg):").pack(pady=5)
        self.entry_peso = ttk.Entry(self)
        self.entry_peso.pack()

        ttk.Label(self, text="Nueva Edad (años):").pack(pady=5)
        self.entry_edad = ttk.Entry(self)
        self.entry_edad.pack()

        ttk.Button(self, text="Guardar Cambios", command=self.guardar_cambios).pack(pady=20)

        self.cargar_mascotas()

    def cargar_mascotas(self):
        nombres = self.controlador.obtener_lista_mascotas()
        self.combo_mascotas["values"] = nombres
        if nombres:
            self.combo_mascotas.current(0)
            self.limpiar_casillas()  # Aseguramos que inicie en blanco

    def limpiar_casillas(self, event=None):
        """Borra el contenido de las casillas para que queden limpias al cambiar de mascota."""
        self.entry_peso.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)

    def guardar_cambios(self):
        seleccion = self.combo_mascotas.get()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una mascota primero.")
            return

        # Validación de que las casillas no estén vacías
        if not self.entry_peso.get() or not self.entry_edad.get():
            messagebox.showerror("Error", "No puedes dejar las casillas en blanco.")
            return

        try:
            peso = float(self.entry_peso.get())
            edad = int(self.entry_edad.get())
            self.controlador.actualizar_datos_mascota(seleccion, peso, edad)
            messagebox.showinfo("Éxito", "Datos de la mascota actualizados correctamente.")
            self.parent.actualizar_lista_mascotas()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar números válidos para peso y edad.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controlador = ControladorAplicacion()
        self.title("Sistema de Monitoreo de Mascotas")
        self.geometry("550x680")
        self.simulando = False

        # --- PANEL SUPERIOR: Configuración ---
        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(frame_top, text="⚙️ Añadir Nueva Raza", command=self.abrir_configuracion).pack(side=tk.RIGHT)

        # --- PANEL CENTRAL: Registrar nueva mascota ---
        frame_registro = ttk.LabelFrame(self, text="1. Registrar Mascota")
        frame_registro.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(frame_registro, text="Especie:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_especie = ttk.Combobox(frame_registro, values=["perro", "gato"], state="readonly")
        self.combo_especie.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo_especie.bind("<<ComboboxSelected>>", self.actualizar_razas)

        ttk.Label(frame_registro, text="Raza:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_raza = ttk.Combobox(frame_registro, state="readonly")
        self.combo_raza.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.combo_especie.current(0)
        self.actualizar_razas()

        ttk.Label(frame_registro, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = ttk.Entry(frame_registro)
        self.entry_nombre.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.entry_nombre.bind("<FocusOut>", self.verificar_nombre)

        self.label_apellido = ttk.Label(frame_registro, text="¡Nombre en uso! Añade un Apellido:")
        self.entry_apellido = ttk.Entry(frame_registro)

        ttk.Label(frame_registro, text="Peso (kg):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_peso = ttk.Entry(frame_registro)
        self.entry_peso.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_registro, text="Edad (años):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_edad = ttk.Entry(frame_registro)
        self.entry_edad.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(frame_registro, text="Registrar", command=self.registrar).grid(row=6, column=0, columnspan=2,
                                                                                  pady=10)

        # --- PANEL INFERIOR: Monitoreo Simulado ---
        frame_monitoreo = ttk.LabelFrame(self, text="2. Monitoreo Ambiental (Simulación)")
        frame_monitoreo.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(frame_monitoreo, text="Seleccionar Mascota:").pack(pady=5)

        frame_combo_mascotas = ttk.Frame(frame_monitoreo)
        frame_combo_mascotas.pack()

        self.combo_mascotas = ttk.Combobox(frame_combo_mascotas, state="readonly", width=25)
        self.combo_mascotas.pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_combo_mascotas, text="Modificar", command=self.abrir_modificar_mascota).pack(side=tk.LEFT,
                                                                                                         padx=5)

        self.actualizar_lista_mascotas()

        frame_botones_sim = ttk.Frame(frame_monitoreo)
        frame_botones_sim.pack(pady=10)
        self.btn_iniciar = ttk.Button(frame_botones_sim, text="▶ Iniciar Monitoreo", command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        self.btn_detener = ttk.Button(frame_botones_sim, text="⏹ Detener", command=self.detener_simulacion,
                                      state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=5)

        # Pantalla de resultados
        self.lbl_resultado = tk.Label(frame_monitoreo, text="Esperando...", font=("Arial", 11), bg="black", fg="lime",
                                      width=40, height=4)
        self.lbl_resultado.pack(pady=5)

    def abrir_configuracion(self):
        VentanaConfiguracion(self, self.controlador)

    def abrir_modificar_mascota(self):
        VentanaModificarMascota(self, self.controlador)

    def actualizar_razas(self, event=None):
        especie = self.combo_especie.get()
        if not especie: return
        razas = self.controlador.obtener_lista_razas(especie)
        self.combo_raza["values"] = razas
        if razas:
            self.combo_raza.current(0)
        else:
            self.combo_raza.set("Criollo")

    def actualizar_lista_mascotas(self):
        nombres = self.controlador.obtener_lista_mascotas()
        self.combo_mascotas["values"] = nombres
        if nombres:
            self.combo_mascotas.current(0)

    def verificar_nombre(self, event=None):
        nombre = self.entry_nombre.get()
        especie = self.combo_especie.get()
        if nombre and especie:
            if self.controlador.verificar_nombre_existente(nombre, especie):
                self.label_apellido.grid(row=3, column=0, padx=5, pady=5, sticky="e")
                self.entry_apellido.grid(row=3, column=1, padx=5, pady=5, sticky="w")
            else:
                self.label_apellido.grid_remove()
                self.entry_apellido.grid_remove()

    def registrar(self):
        try:
            self.controlador.registrar_mascota(
                self.combo_especie.get(), self.entry_nombre.get(),
                float(self.entry_peso.get()), int(self.entry_edad.get()),
                self.combo_raza.get(), self.entry_apellido.get()
            )
            messagebox.showinfo("Éxito", "Mascota guardada.")
            self.actualizar_lista_mascotas()

            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_peso.delete(0, tk.END)
            self.entry_edad.delete(0, tk.END)
            self.label_apellido.grid_remove()
            self.entry_apellido.grid_remove()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def iniciar_simulacion(self):
        if not self.combo_mascotas.get():
            messagebox.showwarning("Atención", "Primero debes registrar o seleccionar una mascota.")
            return

        self.simulando = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        self.combo_mascotas.config(state=tk.DISABLED)
        self.ciclo_simulacion()

    def detener_simulacion(self):
        self.simulando = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.combo_mascotas.config(state="readonly")
        self.lbl_resultado.config(text="Simulación detenida.", fg="lime")

    def ciclo_simulacion(self):
        if not self.simulando:
            return

        nombre = self.combo_mascotas.get()
        mediciones, eval = self.controlador.simular_monitoreo(nombre)

        texto = f"Temp: {mediciones['temperatura']}°C  [{eval['temperatura']}]\n"
        texto += f"Hum: {mediciones['humedad']}%  [{eval['humedad']}]\n"

        if eval["apto"]:
            texto += "ESTADO: AMBIENTE ÓPTIMO"
            self.lbl_resultado.config(text=texto, fg="lime")
        else:
            texto += "ESTADO: ¡ALERTA AMBIENTAL!"
            self.lbl_resultado.config(text=texto, fg="red")

        self.after(3000, self.ciclo_simulacion)
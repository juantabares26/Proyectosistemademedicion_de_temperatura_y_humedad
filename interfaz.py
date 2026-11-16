import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil
import os
from controlador import ControladorAplicacion


class VentanaConfiguracion(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador
        self.title("Añadir Raza")
        self.geometry("300x350")
        self.grab_set()

        # Adquiere el color de fondo de la ventana principal para coincidir con el modo actual
        self.configure(bg=parent.cget("bg"))

        try:
            self.iconbitmap("huella.ico")
        except:
            pass

        ttk.Label(self, text="Especie:").pack(pady=5)

        frame_radio_conf = ttk.Frame(self)
        frame_radio_conf.pack()
        self.var_especie = tk.StringVar(value="perro")
        self.rb_perro = ttk.Radiobutton(frame_radio_conf, text="Perro 🐶", variable=self.var_especie, value="perro")
        self.rb_perro.pack(side=tk.LEFT, padx=5)
        self.rb_gato = ttk.Radiobutton(frame_radio_conf, text="Gato 🐱", variable=self.var_especie, value="gato")
        self.rb_gato.pack(side=tk.LEFT, padx=5)

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
                self.var_especie.get(), self.entry_raza.get(),
                self.entry_tmin.get(), self.entry_tmax.get(),
                self.entry_hmin.get(), self.entry_hmax.get()
            )
            messagebox.showinfo("Éxito", "Raza guardada en el Excel.")
            self.parent.actualizar_razas()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class VentanaModificarRaza(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.parent = parent
        self.controlador = controlador
        self.title("Modificar Raza")
        self.geometry("300x420")
        self.grab_set()

        self.configure(bg=parent.cget("bg"))

        try:
            self.iconbitmap("huella.ico")
        except:
            pass

        ttk.Label(self, text="Especie:").pack(pady=5)
        frame_radio = ttk.Frame(self)
        frame_radio.pack()
        self.var_especie = tk.StringVar(value="perro")
        ttk.Radiobutton(frame_radio, text="Perro", variable=self.var_especie, value="perro",
                        command=self.cargar_lista_razas).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_radio, text="Gato", variable=self.var_especie, value="gato",
                        command=self.cargar_lista_razas).pack(side=tk.LEFT, padx=5)

        ttk.Label(self, text="Seleccionar Raza a Modificar:").pack(pady=5)
        self.combo_raza = ttk.Combobox(self, state="readonly")
        self.combo_raza.pack()
        self.combo_raza.bind("<<ComboboxSelected>>", self.cargar_datos_raza)

        ttk.Label(self, text="Nuevo Nombre de la Raza:").pack(pady=5)
        self.entry_nuevo_nombre = ttk.Entry(self)
        self.entry_nuevo_nombre.pack()

        ttk.Label(self, text="Nuevos Valores Temp (°C):").pack(pady=5)
        frame_temp = ttk.Frame(self)
        frame_temp.pack()
        self.entry_tmin = ttk.Entry(frame_temp, width=7)
        self.entry_tmin.pack(side=tk.LEFT, padx=5)
        self.entry_tmax = ttk.Entry(frame_temp, width=7)
        self.entry_tmax.pack(side=tk.LEFT, padx=5)

        ttk.Label(self, text="Nuevos Valores Humedad (%):").pack(pady=5)
        frame_hum = ttk.Frame(self)
        frame_hum.pack()
        self.entry_hmin = ttk.Entry(frame_hum, width=7)
        self.entry_hmin.pack(side=tk.LEFT, padx=5)
        self.entry_hmax = ttk.Entry(frame_hum, width=7)
        self.entry_hmax.pack(side=tk.LEFT, padx=5)

        ttk.Button(self, text="Guardar Cambios", command=self.modificar).pack(pady=20)
        self.cargar_lista_razas()

    def cargar_lista_razas(self):
        razas = self.controlador.obtener_lista_razas(self.var_especie.get())
        self.combo_raza["values"] = razas
        if razas:
            self.combo_raza.current(0)
            self.cargar_datos_raza()
        else:
            self.combo_raza.set("")
            self.limpiar_casillas()

    def limpiar_casillas(self):
        self.entry_nuevo_nombre.delete(0, tk.END)
        for entry in [self.entry_tmin, self.entry_tmax, self.entry_hmin, self.entry_hmax]:
            entry.delete(0, tk.END)

    def cargar_datos_raza(self, event=None):
        raza_actual = self.combo_raza.get()
        if not raza_actual: return
        datos = self.controlador.obtener_datos_raza(self.var_especie.get(), raza_actual)
        if datos:
            self.limpiar_casillas()
            self.entry_nuevo_nombre.insert(0, raza_actual)
            self.entry_tmin.insert(0, str(datos["t_min"]))
            self.entry_tmax.insert(0, str(datos["t_max"]))
            self.entry_hmin.insert(0, str(datos["h_min"]))
            self.entry_hmax.insert(0, str(datos["h_max"]))

    def modificar(self):
        if not self.combo_raza.get(): return
        if not self.entry_nuevo_nombre.get().strip():
            messagebox.showerror("Error", "El nombre de la raza no puede estar vacío.")
            return

        try:
            self.controlador.modificar_raza(
                self.var_especie.get(),
                self.combo_raza.get(),
                self.entry_nuevo_nombre.get(),
                self.entry_tmin.get(), self.entry_tmax.get(),
                self.entry_hmin.get(), self.entry_hmax.get()
            )
            messagebox.showinfo("Éxito", "Parámetros actualizados en el Excel.")
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

        self.configure(bg=parent.cget("bg"))

        try:
            self.iconbitmap("huella.ico")
        except:
            pass

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
            self.limpiar_casillas()

    def limpiar_casillas(self, event=None):
        self.entry_peso.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)

    def guardar_cambios(self):
        seleccion = self.combo_mascotas.get()
        if not seleccion: return
        if not self.entry_peso.get() or not self.entry_edad.get():
            messagebox.showerror("Error", "No dejes casillas en blanco.")
            return
        try:
            peso = float(self.entry_peso.get())
            edad = int(self.entry_edad.get())
            self.controlador.actualizar_datos_mascota(seleccion, peso, edad)
            messagebox.showinfo("Éxito", "Datos de la mascota actualizados.")
            self.parent.actualizar_lista_mascotas()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controlador = ControladorAplicacion()
        self.title("Sistema de Monitoreo de Mascotas")
        self.geometry("570x680")
        self.simulando = False

        # Variable para controlar el tema (Inicia en Claro)
        self.modo_oscuro = False

        try:
            self.iconbitmap("huella.ico")
        except:
            pass

        self.crear_menu()

        # --- BOTÓN PARA CAMBIAR EL MODO OSCURO ---
        frame_top = ttk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=5)

        self.btn_tema = ttk.Button(frame_top, text="🌙 Modo Oscuro", command=self.toggle_tema)
        self.btn_tema.pack(side=tk.LEFT)
        # ----------------------------------------

        # --- PANEL CENTRAL: Registrar nueva mascota ---
        frame_registro = ttk.LabelFrame(self, text="1. Registrar Mascota")
        frame_registro.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame_registro, text="Especie:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        frame_radio = ttk.Frame(frame_registro)
        frame_radio.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.var_especie = tk.StringVar(value="perro")
        self.rb_perro = ttk.Radiobutton(frame_radio, text="Perro 🐶", variable=self.var_especie, value="perro",
                                        command=self.actualizar_razas)
        self.rb_perro.pack(side=tk.LEFT, padx=5)
        self.rb_gato = ttk.Radiobutton(frame_radio, text="Gato 🐱", variable=self.var_especie, value="gato",
                                       command=self.actualizar_razas)
        self.rb_gato.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_registro, text="Raza:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        frame_botones_raza = ttk.Frame(frame_registro)
        frame_botones_raza.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.combo_raza = ttk.Combobox(frame_botones_raza, state="readonly", width=15)
        self.combo_raza.pack(side=tk.LEFT)

        ttk.Button(frame_botones_raza, text="✏️ Modificar", command=self.abrir_modificar_raza).pack(side=tk.LEFT,
                                                                                                    padx=2)
        ttk.Button(frame_botones_raza, text="🗑️ Borrar", command=self.eliminar_raza_seleccionada).pack(side=tk.LEFT,
                                                                                                       padx=2)
        ttk.Button(frame_botones_raza, text="➕ Añadir", command=self.abrir_configuracion).pack(side=tk.LEFT, padx=2)

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

        ttk.Button(frame_registro, text="Registrar Mascota", command=self.registrar).grid(row=6, column=0, columnspan=2,
                                                                                          pady=10)

        # --- PANEL INFERIOR: Monitoreo Simulado ---
        frame_monitoreo = ttk.LabelFrame(self, text="2. Monitoreo Ambiental (Simulación)")
        frame_monitoreo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame_monitoreo, text="Seleccionar Mascota:").pack(pady=5)

        frame_combo_mascotas = ttk.Frame(frame_monitoreo)
        frame_combo_mascotas.pack()

        self.combo_mascotas = ttk.Combobox(frame_combo_mascotas, state="readonly", width=25)
        self.combo_mascotas.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_combo_mascotas, text="✏️ Modificar Mascota", command=self.abrir_modificar_mascota).pack(
            side=tk.LEFT, padx=5)

        self.actualizar_lista_mascotas()

        frame_botones_sim = ttk.Frame(frame_monitoreo)
        frame_botones_sim.pack(pady=10)
        self.btn_iniciar = ttk.Button(frame_botones_sim, text="▶ Iniciar Monitoreo", command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        self.btn_detener = ttk.Button(frame_botones_sim, text="⏹ Detener", command=self.detener_simulacion,
                                      state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=5)

        self.lbl_resultado = tk.Label(frame_monitoreo, text="Esperando...", font=("Arial", 11), bg="black", fg="lime",
                                      width=40, height=4)
        self.lbl_resultado.pack(pady=5)

        # Aplicar el tema inicial (Modo claro por defecto)
        self.aplicar_tema()

    # --- FUNCIONES DEL TEMA (MODO OSCURO/CLARO) ---
    def toggle_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def aplicar_tema(self):
        style = ttk.Style()
        # Usamos el tema 'clam' porque permite modificar colores de forma limpia
        if 'clam' in style.theme_names():
            style.theme_use('clam')

        if self.modo_oscuro:
            # Colores Modo Oscuro
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            btn_bg = "#404040"
            btn_fg = "#ffffff"
            field_bg = "#555555"
            self.btn_tema.config(text="☀️ Modo Claro")
        else:
            # Colores Modo Claro
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            btn_bg = "#e0e0e0"
            btn_fg = "#000000"
            field_bg = "#ffffff"
            self.btn_tema.config(text="🌙 Modo Oscuro")

        # Fondo principal
        self.configure(bg=bg_color)

        # Configuración global de estilos
        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color)
        style.configure("TRadiobutton", background=bg_color, foreground=fg_color)

        style.configure("TButton", background=btn_bg, foreground=btn_fg)
        style.configure("TEntry", fieldbackground=field_bg, foreground=fg_color)
        style.configure("TCombobox", fieldbackground=field_bg, foreground=fg_color)

        # Color del botón al pasar el mouse por encima
        style.map("TButton", background=[("active", "#666666" if self.modo_oscuro else "#d0d0d0")])
        style.map("TCombobox", fieldbackground=[("readonly", field_bg)], foreground=[("readonly", fg_color)])

    # ---------------------------------------------

    def crear_menu(self):
        barra_menu = tk.Menu(self)
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Exportar Backup (Mascotas)...", command=self.exportar_backup)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        self.config(menu=barra_menu)

    def exportar_backup(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")],
            title="Guardar Copia de Seguridad"
        )
        if ruta:
            try:
                shutil.copy("mascotas.json", ruta)
                messagebox.showinfo("Éxito", f"Backup guardado exitosamente en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def abrir_configuracion(self):
        VentanaConfiguracion(self, self.controlador)

    def abrir_modificar_raza(self):
        VentanaModificarRaza(self, self.controlador)

    def abrir_modificar_mascota(self):
        VentanaModificarMascota(self, self.controlador)

    def eliminar_raza_seleccionada(self):
        raza = self.combo_raza.get()
        if not raza:
            messagebox.showwarning("Atención", "Selecciona una raza primero.")
            return

        respuesta = messagebox.askyesno("Confirmar",
                                        f"¿Estás seguro de que deseas eliminar permanentemente la raza '{raza}'?")

        if respuesta:
            try:
                self.controlador.eliminar_raza(self.var_especie.get(), raza)
                messagebox.showinfo("Éxito", f"La raza '{raza}' ha sido eliminada.")
                self.actualizar_razas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la raza:\n{str(e)}")

    def actualizar_razas(self, event=None):
        especie = self.var_especie.get()
        if not especie: return
        razas = self.controlador.obtener_lista_razas(especie)
        self.combo_raza["values"] = razas
        if razas:
            self.combo_raza.current(0)
        else:
            self.combo_raza.set("")

    def actualizar_lista_mascotas(self):
        nombres = self.controlador.obtener_lista_mascotas()
        self.combo_mascotas["values"] = nombres
        if nombres:
            self.combo_mascotas.current(0)

    def verificar_nombre(self, event=None):
        nombre = self.entry_nombre.get()
        especie = self.var_especie.get()
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
                self.var_especie.get(),
                self.entry_nombre.get(),
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
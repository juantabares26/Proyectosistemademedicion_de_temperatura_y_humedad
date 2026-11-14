from animal import Animal
from perro import Perro
from gato import Gato
from sensorAmbiente import SensorAmbiental
from evaluacionAmbiente import EvaluadorAmbiente
from mascotas import GestorMascotas


try:
    gestor = GestorMascotas()
    sensor = SensorAmbiental()
    evaluador = EvaluadorAmbiente()

    print("\n=== SISTEMA DE MONITOREO AMBIENTAL ===")

    mascotas_guardadas = gestor.listar_mascotas()

    if mascotas_guardadas:
        print("\nMascotas registradas:")

        for mascota in mascotas_guardadas:
            print(
                f"- {mascota['nombre']} "
                f"({mascota['tipo']})"
            )

    opcion = input(
        "\n¿Desea usar una mascota registrada? (si/no): "
    ).strip().lower()

    if opcion == "si":
        nombre = input("Nombre de la mascota: ").strip()
        datos = gestor.buscar_por_nombre(nombre)

        if datos is None:
            raise ValueError("No se encontró la mascota registrada.")

        if datos["tipo"] == "perro":
            animal = Perro(
                datos["nombre"],
                datos["peso"],
                datos["edad"]
            )
        elif datos["tipo"] == "gato":
            animal = Gato(
                datos["nombre"],
                datos["peso"],
                datos["edad"]
            )
        else:
            raise ValueError("El tipo de animal guardado no es válido.")

    elif opcion == "no":
        tipo = input(
            "Tipo de animal (perro/gato): "
        ).strip().lower()

        if tipo not in ("perro", "gato"):
            raise ValueError("Debe seleccionar perro o gato.")

        nombre = input("Nombre de la mascota: ").strip()
        peso = float(input("Peso en kilogramos: "))
        edad = int(input("Edad en años: "))

        if tipo == "perro":
            animal = Perro(nombre, peso, edad)
        else:
            animal = Gato(nombre, peso, edad)

        gestor.registrar_mascota(animal)

        print("\nMascota registrada correctamente.")

    else:
        raise ValueError("Esta opción no es válida.")

    print("\n=== DATOS DE LA MASCOTA ===")
    print(f"Nombre: {animal.get_nombre()}")
    print(f"Tipo: {animal.tipo_animal().capitalize()}")
    print(f"Peso: {animal.get_peso():.2f} kg")
    print(f"Edad: {animal.get_edad()} años")

    print("\n=== MEDICIONES AMBIENTALES ===")
    mediciones = sensor.leer_mediciones()

    resultado = evaluador.evaluar_ambiente(
        animal,
        mediciones
    )

    print("\n=== RESULTADO ===")
    print(f"Temperatura: {mediciones['temperatura']} °C")
    print(f"Humedad: {mediciones['humedad']} %")
    print(
        f"Estado de la temperatura: "
        f"{resultado['temperatura']}"
    )
    print(
        f"Estado de la humedad: "
        f"{resultado['humedad']}"
    )

    if resultado["apto"]:
        print("El ambiente está dentro de los rangos de referencia.")
    else:
        print("El ambiente está fuera de uno o más rangos de referencia.")

except (ValueError, TypeError) as error:
    print(f"Error en los datos: {error}")

except OSError as error:
    print(f"Error al acceder a los archivos: {error}")

except Exception as error:
    print(f"Se produjo un error inesperado: {error}")
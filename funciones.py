import csv
import json
import random
import re
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TXT_DIR = DATA_DIR / "txt"
CSV_DIR = DATA_DIR / "csv"
JSON_DIR = DATA_DIR / "json"
RESULTADOS_DIR = BASE_DIR / "resultados"
LOG_FILE = BASE_DIR / "log.txt"


def crear_carpetas():
    """Crea las carpetas necesarias si todavía no existen."""
    for carpeta in [TXT_DIR, CSV_DIR, JSON_DIR, RESULTADOS_DIR]:
        carpeta.mkdir(parents=True, exist_ok=True)


def registrar_log(mensaje):
    """Guarda fecha, hora y acción realizada en log.txt."""
    crear_carpetas()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")


def generar_datos(cantidad=50):
    """Genera registros aleatorios con los formatos solicitados."""
    registros = []

    for i in range(1, cantidad + 1):
        edad = random.randint(18, 80)
        frecuencia = random.randint(50, 120)
        saturacion = random.randint(90, 100)

        registro = {
            "id": f"ID-{i:03d}",
            "fr": f"{edad} Años",
            "fc": f"{frecuencia:03d}ppm",
            "spo2": f"{saturacion}%"
        }
        registros.append(registro)

    registrar_log(f"Se generaron {cantidad} registros aleatorios.")
    return registros


def ordenar_datos(registros):
    """Ordena de menor a mayor según la frecuencia cardíaca."""
    return sorted(registros, key=lambda dato: int(dato["fc"][:3]))


def validar_registro(registro):
    """
    Comprueba que existan los cuatro campos y que cumplan
    exactamente los patrones solicitados en el taller.
    """
    patrones = {
        "id": r"^ID-\d{3}$",
        "fr": r"^\d{2} Años$",
        "fc": r"^\d{3}ppm$",
        "spo2": r"^\d{2,3}%$"
    }

    for campo, patron in patrones.items():
        if campo not in registro:
            return False, f"Falta el campo {campo}."

        if not isinstance(registro[campo], str):
            return False, f"El campo {campo} debe ser texto."

        if re.fullmatch(patron, registro[campo]) is None:
            return False, f"El campo {campo} no cumple el formato."

    return True, "Registro válido."


def validar_lista(registros):
    """Valida todos los registros e informa cuáles presentan errores."""
    errores = []

    for posicion, registro in enumerate(registros, start=1):
        valido, mensaje = validar_registro(registro)
        if not valido:
            errores.append(f"Registro {posicion}: {mensaje}")

    if errores:
        print("\nSe encontraron errores:")
        for error in errores:
            print("-", error)
    else:
        print(f"\nTodos los {len(registros)} registros son válidos.")

    registrar_log(
        f"Validación realizada: {len(registros)} registros, "
        f"{len(errores)} con errores."
    )
    return len(errores) == 0


def ingresar_registro(registros):
    """Solicita un registro manual y lo agrega si pasa la validación."""
    print("\nIngrese los datos con el formato indicado.")
    nuevo = {
        "id": input("Identificación (ej. ID-051): ").strip(),
        "fr": input("Edad (ej. 18 Años): ").strip(),
        "fc": input("Frecuencia cardíaca (ej. 090ppm): ").strip(),
        "spo2": input("Saturación (ej. 95%): ").strip()
    }

    valido, mensaje = validar_registro(nuevo)

    if valido:
        if any(dato["id"] == nuevo["id"] for dato in registros):
            print("Ya existe un registro con esa identificación.")
            return registros

        registros.append(nuevo)
        print("Registro agregado correctamente.")
        registrar_log(f"Se ingresó manualmente el registro {nuevo['id']}.")
    else:
        print("No se agregó el registro:", mensaje)

    return registros


def exportar_txt(registros):
    """Guarda los registros en un archivo de texto."""
    crear_carpetas()
    ruta = TXT_DIR / "signos_vitales.txt"

    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write("id|fr|fc|spo2\n")
        for dato in registros:
            archivo.write(
                f'{dato["id"]}|{dato["fr"]}|{dato["fc"]}|{dato["spo2"]}\n'
            )

    registrar_log(f"Datos exportados a TXT: {ruta}")
    print(f"Archivo TXT guardado en: {ruta}")


def exportar_csv(registros):
    """Guarda los registros en formato CSV."""
    crear_carpetas()
    ruta = CSV_DIR / "signos_vitales.csv"

    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        campos = ["id", "fr", "fc", "spo2"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    registrar_log(f"Datos exportados a CSV: {ruta}")
    print(f"Archivo CSV guardado en: {ruta}")


def exportar_json(registros):
    """Guarda los registros en formato JSON."""
    crear_carpetas()
    ruta = JSON_DIR / "signos_vitales.json"

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, indent=4, ensure_ascii=False)

    registrar_log(f"Datos exportados a JSON: {ruta}")
    print(f"Archivo JSON guardado en: {ruta}")


def exportar_todos(registros):
    """Exporta la lista a los tres formatos solicitados."""
    registros = ordenar_datos(registros)
    exportar_txt(registros)
    exportar_csv(registros)
    exportar_json(registros)


def importar_json():
    """Lee los registros desde el archivo JSON."""
    ruta = JSON_DIR / "signos_vitales.json"

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El JSON debe contener una lista de registros.")

        print(f"Se importaron {len(datos)} registros desde JSON.")
        registrar_log(f"Importación JSON: {len(datos)} registros.")
        return datos

    except FileNotFoundError:
        print("No existe el archivo JSON. Exporte los datos primero.")
    except (json.JSONDecodeError, ValueError) as error:
        print("No se pudo leer el JSON:", error)
    except OSError as error:
        print("Error al acceder al archivo:", error)

    return None


def importar_csv():
    """Lee los registros desde el archivo CSV."""
    ruta = CSV_DIR / "signos_vitales.csv"

    try:
        with ruta.open("r", newline="", encoding="utf-8") as archivo:
            datos = list(csv.DictReader(archivo))

        print(f"Se importaron {len(datos)} registros desde CSV.")
        registrar_log(f"Importación CSV: {len(datos)} registros.")
        return datos

    except FileNotFoundError:
        print("No existe el archivo CSV. Exporte los datos primero.")
    except (OSError, csv.Error) as error:
        print("Error al leer el CSV:", error)

    return None


def importar_txt():
    """Lee los registros del TXT separado por el carácter |."""
    ruta = TXT_DIR / "signos_vitales.txt"
    datos = []

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            encabezado = archivo.readline().strip()

            if encabezado != "id|fr|fc|spo2":
                raise ValueError("El encabezado del TXT no es correcto.")

            for linea in archivo:
                partes = linea.strip().split("|")
                if len(partes) == 4:
                    datos.append({
                        "id": partes[0],
                        "fr": partes[1],
                        "fc": partes[2],
                        "spo2": partes[3]
                    })

        print(f"Se importaron {len(datos)} registros desde TXT.")
        registrar_log(f"Importación TXT: {len(datos)} registros.")
        return datos

    except FileNotFoundError:
        print("No existe el archivo TXT. Exporte los datos primero.")
    except (OSError, ValueError) as error:
        print("Error al leer el TXT:", error)

    return None

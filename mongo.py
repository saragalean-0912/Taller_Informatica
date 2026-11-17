import json
import os
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

BASE_DIR = Path(__file__).resolve().parent
RESULTADOS_DIR = BASE_DIR / "resultados"
LOG_FILE = BASE_DIR / "log.txt"


def registrar_log(mensaje):
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")


def conectar_mongodb():
    """
    Se conecta usando la variable de entorno MONGODB_URI.
    La dirección privada de Atlas no debe escribirse en el código
    ni publicarse en GitHub.
    """
    uri = os.getenv("MONGODB_URI")

    if not uri:
        print("No se encontró la variable de entorno MONGODB_URI.")
        print("Configúrala con la dirección de conexión de MongoDB Atlas.")
        return None, None

    try:
        cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
        cliente.admin.command("ping")

        base_datos = cliente["informatica1"]
        coleccion = base_datos["signos vitales"]

        print("Conexión con MongoDB Atlas exitosa.")
        registrar_log("Conexión exitosa con MongoDB Atlas.")
        return cliente, coleccion

    except (PyMongoError, ServerSelectionTimeoutError) as error:
        print("No fue posible conectar con MongoDB:", error)
        return None, None


def insertar_registros(coleccion, registros):
    """Inserta únicamente registros que cumplan los formatos."""
    if coleccion is None:
        print("Primero debe conectarse a MongoDB.")
        return

    if not registros:
        print("No hay registros para insertar.")
        return

    documentos = []

    for registro in registros:
        patrones_validos = (
            len(registro.get("id", "")) == 6
            and registro["id"].startswith("ID-")
            and registro["id"][3:].isdigit()
            and registro.get("fr", "").endswith(" Años")
            and registro.get("fc", "").endswith("ppm")
            and registro.get("spo2", "").endswith("%")
        )

        if patrones_validos:
            documentos.append(registro)

    if not documentos:
        print("No hay registros válidos para insertar.")
        return

    try:
        # Evita duplicar identificaciones que ya existan.
        ids_existentes = set(
            coleccion.distinct("id", {"id": {"$in": [d["id"] for d in documentos]}})
        )
        nuevos = [d for d in documentos if d["id"] not in ids_existentes]

        if nuevos:
            coleccion.insert_many(nuevos)
            print(f"Se insertaron {len(nuevos)} registros.")
        else:
            print("Todos esos registros ya estaban almacenados.")

        registrar_log(f"Intento de inserción: {len(nuevos)} registros nuevos.")

    except PyMongoError as error:
        print("Error al insertar:", error)


def consultar_promedio(coleccion):
    """Calcula el promedio de frecuencia cardíaca."""
    if coleccion is None:
        print("Primero debe conectarse a MongoDB.")
        return None

    pipeline = [
        {
            "$group": {
                "_id": None,
                "promedio_fc": {
                    "$avg": {
                        "$convert": {
                            "input": {"$substrBytes": ["$fc", 0, 3]},
                            "to": "double",
                            "onError": None,
                            "onNull": None
                        }
                    }
                }
            }
        }
    ]

    try:
        resultado = list(coleccion.aggregate(pipeline))
        if resultado and resultado[0]["promedio_fc"] is not None:
            promedio = resultado[0]["promedio_fc"]
            print(f"Promedio de frecuencia cardíaca: {promedio:.2f} ppm")
            return promedio

        print("No hay datos suficientes para calcular el promedio.")
        return None

    except PyMongoError as error:
        print("Error en la consulta:", error)
        return None


def consultar_spo2_baja(coleccion):
    """Busca documentos cuya saturación sea menor a 94%."""
    if coleccion is None:
        print("Primero debe conectarse a MongoDB.")
        return []

    consulta = {
        "$expr": {
            "$lt": [
                {
                    "$convert": {
                        "input": {
                            "$replaceOne": {
                                "input": "$spo2",
                                "find": "%",
                                "replacement": ""
                            }
                        },
                        "to": "int",
                        "onError": 999,
                        "onNull": 999
                    }
                },
                94
            ]
        }
    }

    try:
        documentos = list(coleccion.find(consulta, {"_id": 0}))
        print(f"Documentos encontrados con SpO2 menor a 94%: {len(documentos)}")
        for documento in documentos:
            print(documento)
        return documentos

    except PyMongoError as error:
        print("Error en la consulta:", error)
        return []


def consultar_por_id(coleccion):
    """Busca un registro específico por su identificación."""
    if coleccion is None:
        print("Primero debe conectarse a MongoDB.")
        return None

    identificacion = input("Ingrese el ID que desea buscar (ej. ID-001): ").strip()

    try:
        documento = coleccion.find_one({"id": identificacion}, {"_id": 0})

        if documento:
            print("Registro encontrado:")
            print(documento)
        else:
            print("No existe un registro con esa identificación.")

        return documento

    except PyMongoError as error:
        print("Error en la consulta:", error)
        return None


def exportar_consultas_json(coleccion):
    """Exporta a resultados/mongo.json los resultados de las consultas."""
    if coleccion is None:
        print("Primero debe conectarse a MongoDB.")
        return

    promedio = consultar_promedio(coleccion)
    documentos_bajos = consultar_spo2_baja(coleccion)

    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = RESULTADOS_DIR / "mongo.json"

    resultado = {
        "promedio_frecuencia_cardiaca": promedio,
        "documentos_spo2_menor_94": documentos_bajos
    }

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(resultado, archivo, indent=4, ensure_ascii=False)

    registrar_log("Consultas de MongoDB exportadas a resultados/mongo.json.")
    print(f"Resultados guardados en: {ruta}")

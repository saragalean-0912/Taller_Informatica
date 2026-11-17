from funciones import (
    crear_carpetas,
    generar_datos,
    ordenar_datos,
    validar_lista,
    ingresar_registro,
    exportar_todos,
    importar_json,
    importar_csv,
    importar_txt,
    registrar_log
)
import mongo


def mostrar_menu():
    print("\n========== SISTEMA DE SIGNOS VITALES ==========")
    print("1. Generar 50 registros aleatorios")
    print("2. Ingresar un registro manualmente")
    print("3. Mostrar registros")
    print("4. Ordenar registros por frecuencia cardíaca")
    print("5. Validar registros")
    print("6. Exportar datos a TXT, CSV y JSON")
    print("7. Importar datos desde TXT, CSV o JSON")
    print("8. Conectar con MongoDB Atlas")
    print("9. Insertar registros en MongoDB")
    print("10. Consultar promedio de frecuencia cardíaca")
    print("11. Consultar registros con SpO2 menor a 94%")
    print("12. Buscar registro en MongoDB por ID")
    print("13. Exportar consultas de MongoDB a JSON")
    print("0. Salir")
    print("================================================")


def seleccionar_importacion():
    print("\n¿Qué formato desea importar?")
    print("1. TXT")
    print("2. CSV")
    print("3. JSON")
    opcion = input("Seleccione: ").strip()

    if opcion == "1":
        return importar_txt()
    elif opcion == "2":
        return importar_csv()
    elif opcion == "3":
        return importar_json()
    else:
        print("Opción no válida.")
        return None


def main():
    crear_carpetas()

    registros = []
    cliente = None
    coleccion = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registros = generar_datos(50)
            registros = ordenar_datos(registros)
            print("Se generaron 50 registros y quedaron ordenados.")

        elif opcion == "2":
            registros = ingresar_registro(registros)

        elif opcion == "3":
            if registros:
                for registro in registros:
                    print(registro)
                print(f"Total de registros: {len(registros)}")
            else:
                print("Todavía no hay registros cargados.")

        elif opcion == "4":
            if registros:
                registros = ordenar_datos(registros)
                print("Registros ordenados correctamente.")
            else:
                print("Primero genere o importe los registros.")

        elif opcion == "5":
            if registros:
                validar_lista(registros)
            else:
                print("No hay registros para validar.")

        elif opcion == "6":
            if registros:
                if validar_lista(registros):
                    exportar_todos(registros)
                else:
                    print("Corrija los registros antes de exportarlos.")
            else:
                print("No hay registros para exportar.")

        elif opcion == "7":
            datos_importados = seleccionar_importacion()
            if datos_importados is not None:
                registros = datos_importados
                print("Los datos importados quedaron cargados en el programa.")

        elif opcion == "8":
            if cliente is not None:
                print("Ya existe una conexión abierta.")
            else:
                cliente, coleccion = mongo.conectar_mongodb()

        elif opcion == "9":
            if registros:
                if validar_lista(registros):
                    if coleccion is None:
                        print("Primero conecte con MongoDB (opción 8).")
                    else:
                        mongo.insertar_registros(coleccion, registros)
            else:
                print("Primero genere o importe registros.")

        elif opcion == "10":
            mongo.consultar_promedio(coleccion)

        elif opcion == "11":
            mongo.consultar_spo2_baja(coleccion)

        elif opcion == "12":
            mongo.consultar_por_id(coleccion)

        elif opcion == "13":
            mongo.exportar_consultas_json(coleccion)

        elif opcion == "0":
            if cliente is not None:
                cliente.close()
            registrar_log("El programa se cerró.")
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()

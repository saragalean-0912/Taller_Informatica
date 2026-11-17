# Explicación del Taller 3 - Informática 1

## ¿Qué hace el proyecto?
El programa crea registros de signos vitales ficticios, los organiza, comprueba sus formatos, los guarda en archivos y permite enviarlos a MongoDB Atlas.

## 1. `main.py`: el programa principal
Es el archivo que se ejecuta. Contiene el menú y mantiene la lista `registros` en memoria mientras el programa está abierto. Cada opción del menú llama una función de `funciones.py` o `mongo.py`.

- `mostrar_menu()`: imprime las opciones.
- `seleccionar_importacion()`: pregunta si se importa TXT, CSV o JSON.
- `main()`: controla el ciclo `while True`, recibe la opción y decide qué hacer.
- `if __name__ == "__main__"`: hace que `main()` se ejecute cuando se abre este archivo directamente.

## 2. `funciones.py`: procesamiento y archivos
### Librerías
- `random`: genera valores aleatorios.
- `csv`: escribe y lee archivos CSV.
- `json`: escribe y lee archivos JSON.
- `re`: comprueba formatos con expresiones regulares.
- `Path` de `pathlib`: construye y administra rutas.
- `datetime`: obtiene la fecha y hora para el log.

### Funciones
- `crear_carpetas()`: crea `data/txt`, `data/csv`, `data/json` y `resultados`. `parents=True` crea carpetas intermedias y `exist_ok=True` evita un error si ya existen.
- `registrar_log(mensaje)`: añade al archivo `log.txt` la fecha, hora y descripción de una acción.
- `generar_datos(cantidad=50)`: repite un ciclo y construye diccionarios con `id`, `fr`, `fc` y `spo2`. `randint(a,b)` genera un entero entre ambos extremos, incluidos.
- `ordenar_datos(registros)`: `sorted()` crea una lista ordenada. `lambda` indica qué valor usar; `int(dato["fc"][:3])` toma los tres primeros caracteres de la frecuencia y los convierte a entero.
- `validar_registro(registro)`: comprueba que estén las claves y que sus valores cumplan los patrones.
- `validar_lista(registros)`: recorre la lista y muestra los registros que no cumplen.
- `ingresar_registro(registros)`: solicita un registro por teclado y lo agrega solo si pasa la validación y su ID no está repetido.
- `exportar_txt`, `exportar_csv`, `exportar_json`: guardan la información en cada formato.
- `exportar_todos`: ordena y llama las tres funciones de exportación.
- `importar_txt`, `importar_csv`, `importar_json`: recuperan los datos desde los archivos correspondientes. Los `try/except` permiten responder a errores como archivo inexistente o JSON dañado.

### ¿Qué es una expresión regular?
Es un patrón que permite verificar si un texto tiene una forma determinada. En `re.fullmatch()` se exige que todo el texto coincida con el patrón:
- `^` inicio del texto.
- `$` final del texto.
- `\d` un dígito.
- `{3}` exactamente tres repeticiones.
- `{2,3}` dos o tres repeticiones.

Por eso `^ID-\d{3}$` acepta `ID-001`, pero no `ID-1` ni `ID-0001`.

## 3. `mongo.py`: base de datos NoSQL
- `MongoClient`: establece la conexión con MongoDB Atlas.
- `MONGODB_URI`: variable de entorno que guarda la cadena privada de conexión.
- `informatica1`: nombre de la base de datos.
- `signos vitales`: nombre de la colección.
- `insertar_registros()`: inserta los registros validados y evita insertar IDs que ya existan.
- `consultar_promedio()`: usa una agregación `$group` y `$avg`. Como `fc` se guarda como texto, extrae sus tres primeros caracteres y los convierte a número.
- `consultar_spo2_baja()`: usa `$expr` para comparar el valor numérico de SpO2 con 94.
- `consultar_por_id()`: busca un documento con `find_one`.
- `exportar_consultas_json()`: guarda el promedio y los documentos con SpO2 menor a 94 en `resultados/mongo.json`.

## 4. ¿Qué es cada formato?
- TXT: archivo de texto plano. En este proyecto los campos están separados por `|`.
- CSV: archivo de valores separados por comas; útil para abrir datos en hojas de cálculo.
- JSON: estructura de datos basada en listas y objetos; se parece a los diccionarios y listas de Python.
- MongoDB: base de datos NoSQL que guarda documentos parecidos a diccionarios de Python.

## 5. Módulos del sistema: `os`, `pathlib` e IO
El taller menciona herramientas del sistema. El proyecto utiliza `pathlib` para crear y manejar rutas, y operaciones de entrada/salida (IO) mediante `open()` y `Path.open()` para leer y escribir archivos. `os` se utiliza en `mongo.py` para leer la variable de entorno con `os.getenv()`. Los archivos se guardan directamente en las carpetas de destino, por lo que no se necesita moverlos después.

## 6. Excepciones
`try` contiene instrucciones que podrían fallar. `except` captura errores esperados y permite mostrar un mensaje en vez de cerrar el programa inesperadamente. Ejemplos: `FileNotFoundError`, `JSONDecodeError`, `OSError` y errores de PyMongo.

## 7. ¿Qué debes revisar antes de entregar?
- Que el programa genere 50 registros.
- Que la frecuencia quede ordenada numéricamente.
- Que se creen los tres formatos.
- Que la importación recupere los registros.
- Que los formatos incorrectos sean rechazados.
- Que `log.txt` registre acciones.
- Que MongoDB conecte, inserte y consulte.
- Que el repositorio de GitHub sea público y tenga cinco commits.

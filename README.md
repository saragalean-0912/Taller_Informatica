# Taller 3 - Informática 1

Sistema de generación, validación, almacenamiento y consulta de registros de signos vitales.

## 1. Requisitos

- Python 3.10 o superior.
- Visual Studio Code.
- Para el punto de MongoDB: una cuenta de MongoDB Atlas y una cadena de conexión.
- La biblioteca `pymongo`.

## 2. Archivos del proyecto

- `main.py`: menú principal y coordinación de las funciones.
- `funciones.py`: generación, ordenamiento, validación y manejo de TXT, CSV y JSON.
- `mongo.py`: conexión, inserción y consultas en MongoDB Atlas.
- `data/txt`: archivos de texto.
- `data/csv`: archivos CSV.
- `data/json`: archivos JSON.
- `resultados/mongo.json`: resultados de las consultas de MongoDB.
- `log.txt`: historial de acciones.

## 3. Instalación

Abra la carpeta del proyecto en Visual Studio Code. Abra la terminal y ejecute:

```bash
python -m pip install -r requirements.txt
```

## 4. Ejecutar el programa

En la terminal, desde la carpeta del proyecto:

```bash
python main.py
```

Primero seleccione la opción 1 para generar los 50 registros. Después puede validarlos con la opción 5 y exportarlos con la opción 6.

## 5. Configurar MongoDB Atlas

1. Cree un clúster gratuito en MongoDB Atlas.
2. Cree un usuario de base de datos y configure el acceso de red.
3. Copie la cadena de conexión de Python.
4. Configure esa cadena en la variable de entorno `MONGODB_URI`. Reemplace `<password>` por la contraseña del usuario de base de datos y seleccione el nombre de su clúster.

En PowerShell, para la sesión actual:

```powershell
$env:MONGODB_URI="mongodb+srv://USUARIO:CONTRASENA@CLUSTER.mongodb.net/?retryWrites=true&w=majority"
```

Luego ejecute `python main.py` desde esa misma terminal. No escriba la contraseña directamente en `mongo.py` ni la suba a GitHub.

La base de datos se llama `informatica1` y la colección se llama `signos vitales`.

## 6. Orden recomendado de uso

1. Generar 50 registros.
2. Mostrar y revisar los registros.
3. Validar los datos.
4. Ordenar por frecuencia cardíaca.
5. Exportar a TXT, CSV y JSON.
6. Importar el formato que se quiera comprobar.
7. Configurar MongoDB Atlas.
8. Conectarse a MongoDB.
9. Insertar los registros.
10. Ejecutar las consultas y exportar `resultados/mongo.json`.

## 7. GitHub

Desde la terminal, después de crear un repositorio público vacío en GitHub:

```bash
git init
git add .
git commit -m "Estructura inicial del proyecto"
git add funciones.py
git commit -m "Agrega generacion y validacion de registros"
git add funciones.py
git commit -m "Agrega manejo de archivos TXT CSV y JSON"
git add mongo.py requirements.txt
git commit -m "Integra conexion y consultas de MongoDB"
git add main.py README.md
git commit -m "Integra menu principal y documentacion"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Reemplace la dirección de ejemplo por la URL real de su repositorio.

## 8. Formatos de validación

- `id`: `ID-001` (tres dígitos después de `ID-`).
- `fr`: `18 Años` (dos dígitos, espacio y la palabra Años).
- `fc`: `090ppm` (tres dígitos seguidos de `ppm`).
- `spo2`: `95%` (dos o tres dígitos seguidos de `%`).

Los valores aleatorios se usan para probar el programa y no representan una valoración clínica.

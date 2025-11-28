# Práctica 3.4: JSON y XML

## Identificación de la Actividad

- **ID de la Actividad:** 3.4 JSON y XML
- **Módulo:** PROG
- **Unidad de Trabajo:** U3 – Ficheros, JSON y XML
- **Fecha de Creación:** 28/11/2025
- **Fecha de Entrega:** 30/11/2025
- **Alumno:**
    - **Nombre y Apellidos:** Irene Foncubierta Lobatón
    - **Correo electrónico:** ifonlob1108@g.educaand.es
    - **Iniciales del Alumno/Grupo:** IFL


## Descripción de la Actividad

La práctica consiste en trabajar con ficheros JSON y XML en Python dentro de la Unidad 3 del módulo de Programación.
En concreto, se pide:

- Implementar un programa en Python que gestione usuarios almacenados en un fichero JSON (`leer_json.py`).
- Implementar un programa en Python que trabaje con ficheros XML (`leer_xml.py`).
- Utilizar funciones auxiliares para mejorar la legibilidad (por ejemplo, limpiar la consola y pausar la ejecución).
- Manejar correctamente errores habituales (ficheros inexistentes, formato JSON/XML inválido, estructura sin usuarios, etc.).

El objetivo es practicar: lectura y escritura de ficheros, manejo de estructuras de datos (diccionarios/listas), validación de datos introducidos por el usuario y uso de módulos como `json` o `xml.etree.ElementTree`.

## Instrucciones de Compilación y Ejecución

### 1. Requisitos Previos

- **Lenguaje:** Python 3.11 (o compatible con Python 3.x)
- **Entorno recomendado:**
    - Visual Studio Code / PyCharm / editor de tu preferencia
    - Intérprete de Python instalado en el sistema
- **Dependencias externas:** No se utilizan librerías externas; solo módulos de la librería estándar (`json`, `os`, `xml.etree.ElementTree`, etc.).


### 2. Organización del proyecto

- Carpeta `src/`
    - `leer_json.py` – Programa de gestión de usuarios con JSON
    - `leer_xml.py` – Programa para trabajar con XML
- Carpeta `tests/`
    - Pruebas unitarias asociadas (si se implementan)

Los ficheros de datos (`datos_usuarios_orig.json`, `datos_usuarios.json`, y los XML que se usen) se sitúan en la carpeta raíz del proyecto.

### 3. Ejecución del código

Desde la raíz del proyecto:

```bash
# Ejecutar la parte JSON
python src/leer_json.py

# Ejecutar la parte XML
python src/leer_xml.py
```

Si se desea usar `python3` en lugar de `python` (según sistema):

```bash
python3 src/json.py
python3 src/xml.py
```


### 4. Ejecución de Pruebas

Si se han definido pruebas unitarias en la carpeta `tests/`, se pueden ejecutar con `pytest` o con el framework que se haya elegido. Ejemplo (con `pytest`):

```bash
pytest tests/
```

## Desarrollo de la Actividad

### Descripción del Desarrollo

Para la parte de **JSON (json.py)** se ha desarrollado un programa de “Gestión de usuarios” que trabaja sobre dos ficheros:

- `datos_usuarios_orig.json`: fichero origen con los datos iniciales.
- `datos_usuarios.json`: fichero destino sobre el que se realizan las modificaciones.

Se han implementado, entre otras, las siguientes funciones:

- `limpiar_consola()`: limpia la terminal según el sistema operativo (`cls` en Windows, `clear` en Linux/macOS).
- `inicializar_datos()`:
    - Lee `datos_usuarios_orig.json`.
    - Valida que la estructura contenga la clave `"usuarios"` y que no esté vacía.
    - Maneja errores si el archivo no existe o si el formato JSON es inválido.
    - Copia el contenido al archivo `datos_usuarios.json` y muestra el mensaje de inicialización correcta.
- `mostrar_datos(datos)`:
    - Muestra en consola el contenido de los usuarios con el formato:

```
`ID: <id>, Nombre: <nombre>, Edad: <edad>`  
```

    - Si no hay usuarios, muestra un mensaje de error específico.
- `pausar()`: realiza una pausa hasta que el usuario pulse Enter.
- `modificar_datos(datos)`:
    - Presenta un menú con las opciones: `actualizar`, `insertar`, `eliminar`, `terminar`.
    - **Actualizar**: pide un ID, valida que exista y solicita una nueva edad (número natural razonable).
    - **Insertar**: pide un nuevo ID (numérico y no existente), nombre (solo letras) y edad válida, y añade un nuevo usuario.
    - **Eliminar**: pide un ID y elimina al usuario correspondiente si existe.
    - Tras cada operación muestra los datos actualizados y realiza una pausa.
    - Al elegir `terminar`, guarda de nuevo los datos en `datos_usuarios.json` y muestra un mensaje indicando que el archivo se ha actualizado.

El flujo principal (`main`) limpia la consola, inicializa los datos, muestra el contenido inicial, pausa y luego permite realizar las operaciones de actualización, inserción y eliminación antes de guardar los cambios.

Para la parte de **XML (xml.py)** se ha seguido un enfoque similar (lectura, modificación y escritura del fichero XML) utilizando las herramientas de la librería estándar de Python para procesar XML, manteniendo una estructura clara y funciones separadas por responsabilidad.

Los enlaces al código se han incluido usando enlaces permanentes a los archivos y/o fragmentos concretos de GitHub, tal y como se indica en la documentación oficial de GitHub.

### Código Fuente

Enlaces a los archivos principales del repositorio:

- [src/leer_json.py](https://github.com/IES-Rafael-Alberti/2526-u3-3-4-json-y-xml-ifonlob/blob/0bac1265da6cfc0d74c212f021e0e5542e1db686/src/leer_json.py)` – Gestión de usuarios con JSON 
- [src/leer_xml.py](https://github.com/IES-Rafael-Alberti/2526-u3-3-4-json-y-xml-ifonlob/blob/293e6861f05b28782b88b9b528552b35f48374fd/src/leer_xml.py) – Manejo de Archivos XML



### Ejemplos de Ejecución

**Parte JSON (json.py)**

1. **Inicio del programa**
    - Entrada: ejecución de `python src/json.py` con un `datos_usuarios_orig.json` válido.
    - Salida esperada (resumen):
        - Mensaje de inicialización:
`Datos inicializados desde 'datos_usuarios_orig.json' a 'datos_usuarios.json'.`
        - Listado inicial de usuarios:

```text
--- Contenido Actual del JSON ---
ID: 1, Nombre: Juan, Edad: 30
ID: 2, Nombre: Ana, Edad: 25
--- Fin del Contenido ---
```

        - Pausa: `Presione Enter para continuar...`
2. **Actualizar la edad de un usuario**
    - Entrada: opción `actualizar`, ID `1`, nueva edad `31`.
    - Salida esperada: mensaje de éxito y listado con Juan actualizado.
3. **Insertar un nuevo usuario**
    - Entrada: opción `insertar`, ID `3`, nombre `Pedro`, edad `40`.
    - Salida esperada: mensaje `Usuario Pedro añadido con éxito.` y listado con el nuevo usuario.
4. **Eliminar un usuario**
    - Entrada: opción `eliminar`, ID `2`.
    - Salida esperada: mensaje `Usuario con ID 2 eliminado.` y listado sin Ana.
5. **Guardar y terminar**
    - Entrada: opción `terminar`.
    - Salida esperada: mensaje `Operaciones completadas. Archivo actualizado.`

**Parte XML (xml.py)**
Se pueden describir de forma análoga los casos de prueba: lectura de un XML, modificación de nodos/atributos, y escritura/guardado del resultado.

### Resultados de Pruebas

Se han verificado los siguientes escenarios (de forma manual y/o con pruebas unitarias en `tests/`):

- `datos_usuarios_orig.json` no existe → mensaje:
`ERROR El archivo origen 'datos_usuarios_orig.json' no existe. No se realizó la copia.`
- `datos_usuarios_orig.json` con formato inválido → mensaje:
`ERROR El archivo origen 'datos_usuarios_orig.json' tiene un formato JSON inválido`
- `datos_usuarios_orig.json` sin usuarios (`"usuarios": []`) → mensaje:
`ERROR. El JSON no contiene usuarios.`
- Operaciones sobre usuarios: actualización, inserción y eliminación con IDs válidos e inválidos, comprobando que los mensajes y las validaciones funcionan como se espera.

## Conclusiones

La práctica ha permitido:

- Comprender cómo leer y escribir ficheros JSON y XML con Python.
- Trabajar con diccionarios y listas de diccionarios para representar entidades como “usuarios”.
- Implementar validaciones sencillas sobre los datos introducidos por el usuario (tipos, rangos, unicidad de ID).
- Manejar errores habituales de ficheros (no encontrado, formato inválido) y mostrar mensajes claros en consola.

Como posibles mejoras futuras se podrían añadir más pruebas unitarias automatizadas, validaciones adicionales (por ejemplo, evitar IDs negativos) y una interfaz de menú más estructurada o reutilizable entre las partes JSON y XML.

## Referencias y Fuentes

- [Documentación oficial de Python sobre JSON](https://www.w3schools.com/python/python_json.asp) 
- Material de la Unidad 3: JSON y XML proporcionado por el profesor (enlaces U3: JSON y U3: XML).
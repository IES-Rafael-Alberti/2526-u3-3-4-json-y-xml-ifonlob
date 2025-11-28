import json
import os

def limpiar_consola():
    '''
    Limpia la consola según el sistema operativo.

    Esta función detecta el sistema operativo actual y ejecuta el comando
    correspondiente para limpiar la pantalla de la terminal.
    '''
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
def inicializar_datos()-> dict | None:
    '''
    Inicializa el archivo de trabajo 'datos_usuarios.json' a partir del origen.

    Lee el contenido de ``datos_usuarios_orig.json`` y, si es válido y contiene
    usuarios, lo copia a ``datos_usuarios.json`` sobrescribiendo su contenido.

    Returns
    -------
    dict or None
        Diccionario con los datos cargados si la operación se realiza con éxito.
        Devuelve ``None`` si ocurre algún error o si el JSON de origen no
        contiene usuarios.

    '''
    try:
        with open('./datos_usuarios_orig.json','r') as archivo_original:
            datos = json.load(archivo_original)
            if not datos.get("usuarios"):
                print("ERROR. El JSON no contiene usuarios.")
                return None
    except FileNotFoundError:
        print("ERROR El archivo origen 'datos_usuarios_orig.json' no existe. No se realizó la copia.")
        return None
    except json.JSONDecodeError:
        print("ERROR El archivo origen 'datos_usuarios_orig.json' tiene un formato JSON inválido")
        return None
    try:
        with open('./datos_usuarios.json','w') as archivo:
            json.dump(datos,archivo,indent = 4)
            print("Datos inicializados desde 'datos_usuarios_orig.json' a 'datos_usuarios.json'.")
    except FileNotFoundError:
        print("ERROR El archivo destino 'datos_usuarios' no existe. No se realizó la copia.")
        return None
    except OSError:
        print("Error de escritura en 'datos_usuarios.json'")
        return None
    return datos

def modificar_datos(datos:dict):
    '''
    Permite modificar la lista de usuarios interactuando por consola.

    Muestra un menú con distintas operaciones sobre los usuarios y va
    solicitando datos al usuario hasta que se elija la opción ``terminar``.

    Parámetros
    ----------
    datos : dict
        Diccionario que contiene, al menos, la clave ``"usuarios"`` con una
        lista de diccionarios de usuario. Cada usuario debe tener las claves
        ``"id"``, ``"nombre"`` y ``"edad"``.

    Operaciones
    -----------
    - ``actualizar``: Actualiza la edad de un usuario existente.
    - ``insertar``: Inserta un nuevo usuario con ID único, nombre y edad válidos.
    - ``eliminar``: Elimina un usuario existente por su ID.
    - ``terminar``: Muestra los datos y guarda el JSON en disco.
    '''
    terminado = False
    while not terminado:
        eleccion = input(
            "Introduzca 'actualizar' para actualizar la edad de un usuario, "
            "'insertar' para añadir un nuevo usuario, "
            "'eliminar' para borrar un usuario o "
            "'terminar' para finalizar el programa.\n"
        ).lower()
        while eleccion.lower() != 'actualizar' and eleccion.lower() != 'insertar' and eleccion.lower() != 'eliminar' and eleccion.lower() != 'terminar':
            print("ERROR. Introduzca un valor válido ('actualizar','insertar','eliminar' o 'terminar'.)\n")
            eleccion = input("Introduzca 'actualizar si desea actualizar la edad de un usuario, 'insertar si desea añadir un nuevo usuario,'eliminar' si desea borrar un usuario o 'terminar' para finalizar el programa.\n")
        if eleccion.lower() == 'actualizar':
            usuario_encontrado = False
            while not usuario_encontrado:
                id_usuario = input("Introduzca el ID del usuario al deseas actualizar su edad:\n")
                encontrado = False
                for usuario in datos["usuarios"]:
                    if str(usuario['id']) == id_usuario:
                        edad_actualizada = input("Introduzca ahora la edad actualizada:\n")
                        while not (edad_actualizada.isdigit() and 0 <= int(edad_actualizada) <= 120):
                            print("ERROR. La edad tiene que ser un número natural razonable.")
                            edad_actualizada = input("Introduzca ahora la edad actualizada:\n")
                        usuario['edad'] = int(edad_actualizada)
                        encontrado = True
                if encontrado:
                   usuario_encontrado = True 
                else:
                    print("ERROR. Introduzca un ID de un usuario existente, por favor.")
            print(f"Usuario con ID {id_usuario} actualizado con éxito.")
            mostrar_datos(datos)
            pausar()
        elif eleccion.lower() == 'insertar':
            usuario_existente = True
            while usuario_existente:
                id_usuario_nuevo = input("Introduzca el ID del usuario que deseas añadir:\n")
                while not id_usuario_nuevo.isdigit():
                    print("ERROR. El ID tiene que ser un número natural")
                    id_usuario_nuevo = input("Introduzca el ID del usuario que deseas añadir:\n")
                encontrado = False
                for usuario in datos["usuarios"]:
                    if str(usuario['id']) == id_usuario_nuevo:
                        print("ERROR. El ID introducido ya pertenece a un usuario.")
                        encontrado = True
                if not encontrado:
                    usuario_existente = False
            nombre_nuevo = input("Introduzca ahora el nombre del usuario nuevo.\n")
            while not nombre_nuevo.isalpha():
                print("ERROR. El nombre solo puede contener letras.") 
                nombre_nuevo = input("Introduzca ahora el nombre del usuario nuevo.\n")
            edad_nueva = input("Introduzca ahora la edad del usuario nuevo.\n")
            while not (edad_nueva.isdigit() and 0 <= int(edad_nueva) <= 120):
                print("ERROR. La edad tiene que ser un número natural razonable.")
                edad_nueva = input("Introduzca ahora la edad actualizada:\n")
            nuevo_usuario = {
                "id": int(id_usuario_nuevo),
                "nombre": nombre_nuevo.title(),
                "edad": int(edad_nueva)
            }
            datos["usuarios"].append(nuevo_usuario)
            print(f"Usuario {nombre_nuevo.title()} añadido con éxito.")
            mostrar_datos(datos)
            pausar()
        elif eleccion.lower() == 'eliminar':            
            usuario_encontrado = False
            while not usuario_encontrado:
                id_usuario = input("Introduzca el ID del usuario al deseas eliminar:\n")
                encontrado = False
                for usuario in datos["usuarios"]:
                    if str(usuario['id']) == id_usuario:
                        datos["usuarios"].remove(usuario)
                        encontrado = True
                if encontrado:
                    usuario_encontrado = True
                else:
                    print("ERROR. Introduzca un ID de un usuario existente, por favor.")
            print(f"Usuario con ID {id_usuario} eliminado con éxito.")
            mostrar_datos(datos)
            pausar()
        else: # Terminar
            terminado = True
            mostrar_datos(datos)
            try:
                with open('datos_usuarios.json','w') as archivo:
                    json.dump(datos,archivo,indent=4)
                    print("Operaciones completadas. Archivo actualizado.")
            except OSError:
                print("Error de escritura en 'datos_usuarios.json'")
                return None

def pausar():
    '''
    Realiza una pausa en la ejecución hasta que el usuario pulse Enter.

    La función muestra un mensaje en consola y espera a que el usuario
    presione la tecla Enter antes de continuar con la ejecución del programa.

    '''
    input("Presione Enter para continuar...")
    
def mostrar_datos(datos:dict):
    print("--- Contenido Actual del JSON ---")
    if not datos.get("usuarios"):
        print("ERROR El archivo JSON no contiene usuarios!")
    else:
        for usuario in datos["usuarios"]:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}, Edad: {usuario['edad']}")
    print("--- Fin del Contenido ---")


def main():
    limpiar_consola()
    datos = inicializar_datos()
    if datos is not None:
        mostrar_datos(datos)
    else:
        print("El archivo JSON no existe o es inválido.")
        exit()
    pausar()
    modificar_datos(datos)
    
if __name__ == "__main__":
    main()
import xml.etree.ElementTree as ET
import os

def pausar():
    '''
    Realiza una pausa en la ejecución hasta que el usuario pulse Enter.

    La función muestra un mensaje en consola y espera a que el usuario
    presione la tecla Enter antes de continuar con la ejecución del programa.
    '''
    input("Presione Enter para continuar...")
    
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
def inicializar_datos():
    '''
    Inicializa el archivo XML de trabajo a partir del XML de origen.

    Lee el contenido de ``datos_usuarios_orig.xml`` y, si es válido, lo copia
    al archivo ``datos_usuarios.xml`` sobrescribiendo su contenido. Devuelve
    la raíz del árbol XML cargado para seguir trabajando con él.

    Returns
    -------
    xml.etree.ElementTree.Element or None
        Nodo raíz del XML (por ejemplo, ``<usuarios>``) si la operación se
        realiza con éxito. Devuelve ``None`` si ocurre algún error.
    '''
    try:
        arbol = ET.parse('./datos_usuarios_orig.xml')
        raiz = arbol.getroot()

    except FileNotFoundError:
        print(f"ERROR El archivo origen 'datos_usuarios_orig.xml' no existe. No se realizó la copia.")
        return None
    except ET.ParseError:
        print(f"ERROR El archivo origen 'datos_usuarios_orig.xml' tiene un formato XML inválido.")
        return None
    try:
        arbol = ET.ElementTree(raiz)
        arbol.write("datos_usuarios.xml", encoding="utf-8", xml_declaration=True)
        print("Datos inicializados desde 'datos_usuarios_orig.xml' a 'datos_usuarios.xml'.")
    except FileNotFoundError:
        print("ERROR. La ruta 'datos_usuarios.xml' no es válida. No se realizó la copia.")
        return None
    except PermissionError:
        print("ERROR. No hay permisos para escribir en 'datos_usuarios.xml'.")
        return None
    except OSError:
        print("ERROR. Se produjo un error de escritura en 'datos_usuarios.xml'.")
        return None
    return raiz

def modificar_datos(raiz:ET.Element):
    '''
    Permite modificar los usuarios del XML interactuando por consola.

    Muestra un menú con distintas operaciones sobre los nodos ``<usuario>``
    y va solicitando datos al usuario hasta que se elija la opción
    ``terminar``. Trabaja sobre la raíz del árbol XML en memoria.

    Parameters
    ----------
    raiz : xml.etree.ElementTree.Element
        Nodo raíz del documento XML (normalmente ``<usuarios>``) que contiene
        uno o varios nodos hijo ``<usuario>``.

    Operaciones
    -----------
    - ``actualizar``: Actualiza la edad de un usuario existente por su ID.
    - ``insertar``: Inserta un nuevo usuario con ID único, nombre y edad válidos.
    - ``eliminar``: Elimina un usuario existente por su ID.
    - ``terminar``: Muestra los datos y guarda el XML en ``datos_usuarios.xml``.
    '''
    terminado = False
    while not terminado:
        eleccion = input("Introduzca 'actualizar' si desea actualizar la edad de un usuario, 'insertar' si desea añadir un nuevo usuario,'eliminar' si desea borrar un usuario o 'terminar' para finalizar el programa.\n")
        while eleccion.lower() != 'actualizar' and eleccion.lower() != 'insertar' and eleccion.lower() != 'eliminar' and eleccion.lower() != 'terminar':
            print("ERROR. Introduzca un valor válido ('actualizar','insertar','eliminar' o 'terminar'.)\n")
            eleccion = input("Introduzca 'actualizar si desea actualizar la edad de un usuario, 'insertar si desea añadir un nuevo usuario,'eliminar' si desea borrar un usuario o 'terminar' para finalizar el programa.\n")
        if eleccion.lower() == 'actualizar':
            usuario_encontrado = False
            while not usuario_encontrado:
                id_usuario = input("Introduzca el ID del usuario al deseas actualizar su edad:\n")
                encontrado = False
                for usuario in raiz.findall("usuario"):
                    if usuario.findtext("id") == id_usuario:
                        edad_actualizada = input("Introduzca ahora la edad actualizada:\n")
                        while not (edad_actualizada.isdigit() and 0 <= int(edad_actualizada) <= 120):
                            print("ERROR. La edad tiene que ser un número natural razonable.")
                            edad_actualizada = input("Introduzca ahora la edad actualizada:\n")
                        usuario.find("edad").text = edad_actualizada
                        encontrado = True
                if encontrado:
                   usuario_encontrado = True 
                else:
                    print("ERROR. Introduzca un ID de un usuario existente, por favor.")
            print(f"Usuario con ID {id_usuario} actualizado con éxito.")
            mostrar_datos(raiz)
            pausar()
        elif eleccion.lower() == 'insertar':
            usuario_existente = True
            while usuario_existente:
                id_usuario_nuevo = input("Introduzca el ID del usuario que deseas añadir:\n")
                while not id_usuario_nuevo.isdigit():
                    print("ERROR. El ID tiene que ser un número natural")
                    id_usuario_nuevo = input("Introduzca el ID del usuario que deseas añadir:\n")
                encontrado = False
                for usuario in raiz.findall("usuario"):
                    if usuario.findtext("id") == id_usuario_nuevo:
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
            nuevo = ET.SubElement(raiz,"usuario")
            ET.SubElement(nuevo,"id").text = id_usuario_nuevo
            ET.SubElement(nuevo,"nombre").text = nombre_nuevo
            ET.SubElement(nuevo,"edad").text = edad_nueva
            print(f"Usuario {nombre_nuevo.title()} añadido con éxito.")
            mostrar_datos(raiz)
            pausar()
        elif eleccion.lower() == 'eliminar':            
            usuario_encontrado = False
            while not usuario_encontrado:
                id_usuario = input("Introduzca el ID del usuario al deseas eliminar:\n")
                encontrado = False
                for usuario in raiz.findall("usuario"):
                    if usuario.findtext("id") == id_usuario:
                        raiz.remove(usuario)
                        encontrado = True
                if encontrado:
                    usuario_encontrado = True
                else:
                    print("ERROR. Introduzca un ID de un usuario existente, por favor.")
            print(f"Usuario con ID {id_usuario} eliminado con éxito.")
            mostrar_datos(raiz)
            pausar()
        else: # Terminar
            terminado = True
            mostrar_datos(raiz)
            try:
                arbol = ET.ElementTree(raiz)
                arbol.write("datos_usuarios.xml", encoding="utf-8", xml_declaration=True)
                print("Operaciones completadas. Archivo actualizado.")
            except PermissionError:
                print("ERROR. No hay permisos para escribir en 'datos_usuarios.xml'.")
                return None
            except OSError:
                print("ERROR. Se produjo un error de escritura en 'datos_usuarios.xml'.")
                return None

def mostrar_datos(raiz: ET.Element):
    '''
    Muestra el contenido actual de los usuarios en el XML.

    Recorre todos los nodos ``<usuario>`` hijos de la raíz y muestra sus
    campos ``<id>``, ``<nombre>`` y ``<edad>`` con el formato:

    ``ID: <id>, Nombre: <nombre>, Edad: <edad>``

    Parameters
    ----------
    raiz : xml.etree.ElementTree.Element
        Nodo raíz del documento XML (usualmente ``<usuarios>``), que contiene
        cero o más nodos hijo ``<usuario>``.
    '''
    print("--- Contenido Actual del XML ---")
    usuarios = raiz.findall("usuario")
    if not usuarios:
        print("ERROR No hay usuarios en el archivo XML.")
    else:
        for usuario in usuarios:
            id = usuario.findtext("id")
            nombre = usuario.findtext("nombre")
            edad = usuario.findtext("edad")
            print(f"ID: {id}, Nombre: {nombre}, Edad: {edad}")
    print("--- Fin del Contenido ---")


def main():
    limpiar_consola()
    raiz = inicializar_datos()
    if raiz is not None:
        mostrar_datos(raiz)
    else:
        print("El archivo XML no existe o es inválido.")
        exit()
    pausar()
    modificar_datos(raiz)
    
    
if __name__ == "__main__":
    main()
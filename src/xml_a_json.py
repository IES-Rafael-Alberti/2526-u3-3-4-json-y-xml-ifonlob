import json
import xml.etree.ElementTree as ET

def leer_xml()-> ET.Element | None :
    '''
    Lee el archivo XML de origen y devuelve su raíz.

    Intenta cargar el archivo datos_usuarios_orig.xml utilizando
    xml.etree.ElementTree.parse. Si el archivo existe y tiene un
    formato XML válido, se devuelve el elemento raíz del árbol.

    Returns
    -------
    xml.etree.ElementTree.Element or None
        Raíz del XML si la carga se realiza
        con éxito. Devuelve None si el archivo no existe o tiene un
        formato XML inválido.
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
    return raiz

def transformar_xml_json(raiz:ET.Element):
    '''
    Transforma un fichero XML en una estructura Python apta para JSON.

    Recorre recursivamente el árbol XML a partir del elemento raiz y
    construye una estructura basada en diccionarios, listas y cadenas
    de texto, adecuada para ser serializada con json.dumps.

    La conversión sigue estas reglas:

    - Nodos sin hijos (hojas) se convierten en cadenas con su texto.
    - Nodos con hijos se convierten en diccionarios donde:
      - Cada etiqueta hija es una clave del diccionario.
      - Si una etiqueta aparece una sola vez, su valor es el resultado
        recursivo de ese hijo.
      - Si una etiqueta aparece varias veces, su valor es una lista con
        los resultados de cada hijo.

    Parameters
    ----------
    raiz : xml.etree.ElementTree.Element
        Nodo raíz del subárbol XML que se desea transformar.

    Returns
    -------
    dict or list or str
        Estructura de Python equivalente al contenido de raiz:
        - str si raiz es un nodo hoja.
        - dict si tiene hijos con etiquetas únicas.
        - dict cuyos valores pueden ser listas si hay etiquetas repetidas.
    '''
    hijos = list(raiz)
    if not hijos:
        if raiz.text != None:
            return raiz.text
        else:
            return ""
    resultado = {}
    for hijo in hijos:
        valor = transformar_xml_json(hijo)
        if hijo.tag in resultado:
            if not isinstance(resultado[hijo.tag], list):
                resultado[hijo.tag] = [resultado[hijo.tag]]
            resultado[hijo.tag].append(valor)
        else:
            resultado[hijo.tag] = valor
    return resultado


def main():
    raiz = leer_xml()
    if raiz is None:
        print("ERROR. El archivo XML no existe o es inválido.")
        exit()
    datos = {raiz.tag: transformar_xml_json(raiz)}
    print(json.dumps(datos, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
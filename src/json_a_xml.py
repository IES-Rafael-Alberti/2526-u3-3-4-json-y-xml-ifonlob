import json
import xml.etree.ElementTree as ET

def leer_json()->dict | None:
    '''
    Lee el archivo JSON de origen y devuelve su contenido como diccionario.

    Intenta abrir y cargar el archivo datos_usuarios_orig.json utilizando
    json.load. Si el archivo existe y contiene JSON válido, se devuelve
    el diccionario resultante.

    Returns
    -------
    dict or None
        Diccionario con los datos leídos del JSON si la operación se realiza
        con éxito. Devuelve None si el archivo no existe o si el contenido
        no es JSON válido.

    '''
    try:
        with open('./datos_usuarios_orig.json','r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("ERROR El archivo origen 'datos_usuarios_orig.json' no existe. No se realizó la copia.")
        return None
    except json.JSONDecodeError:
        print("ERROR El archivo origen 'datos_usuarios_orig.json' tiene un formato JSON inválido")
        return None



def json_a_xml(etiqueta: str, valor) -> ET.Element:
    '''
    Convierte un valor JSON en un elemento XML de forma recursiva.

    A partir de una etiqueta y un valor (que puede ser un diccionario,
    una lista o un valor simple), construye un elemento XML usando las
    siguientes reglas:

    - Si ``valor`` es simple (str, int, float, bool, None), se crea
      ``<etiqueta>valor</etiqueta>``.
    - Si ``valor`` es ``dict``, cada par clave-valor se convierte en un
      elemento hijo con la clave como etiqueta.
      - Si el valor asociado a una clave es una lista, se crean varios
        hijos con esa etiqueta (uno por cada elemento de la lista).
    - Si ``valor`` es una lista (caso usado en esta práctica para una lista
      de usuarios), se crean varios elementos ``<usuario>...</usuario>``
      como hijos del elemento actual.

    Parameters
    ----------
    etiqueta : str
        Nombre de la etiqueta XML que se usará para el elemento raíz del
        fragmento que se está generando.
    valor : any
        Valor JSON que se desea transformar. Puede ser un diccionario,
        una lista o un valor simple (cadena, número, etc.).

    Returns
    -------
    xml.etree.ElementTree.Element
        Elemento XML generado a partir del valor proporcionado.
        
    '''
    elemento = ET.Element(etiqueta)
    
    if not isinstance(valor, (dict, list)):
        if valor != None:
            elemento.text = str(valor)
        else:
            elemento.text = ""
        return elemento

    if isinstance(valor, dict):
        for clave, valor in valor.items():
            if isinstance(valor, list):
                for item in valor:
                    elemento.append(json_a_xml(clave, item))
            else:
                elemento.append(json_a_xml(clave, valor))
        return elemento

    for item in valor:
        elemento.append(json_a_xml("usuario", item))
    return elemento



def main():
    datos = leer_json()
    if datos is not None:
        if len(datos) != 1:
            print("ERROR. Se esperaba un único nodo raíz en el JSON.")
            return
    else:
        print("El archivo JSON no existe o es inválido.")
        return
    etiqueta_raiz = None
    valor_raiz = None
    contador = 0
    for clave,valor in datos.items():
        if contador == 0:
            etiqueta_raiz = clave
            valor_raiz = valor
            contador += 1
    raiz_xml = json_a_xml(etiqueta_raiz, valor_raiz)
    arbol = ET.ElementTree(raiz_xml)
    ET.indent(arbol, space="    ", level=0)
    resultado = ET.tostring(raiz_xml, encoding="unicode")
    print(resultado)

if __name__ == "__main__":
    main()
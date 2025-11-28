import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element



def transformar_xml_json(raiz:Element)->dict:
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
    cadena_xml = """
    <usuario>
        <nombre>Juan</nombre>
        <edad>40</edad>
        <habilidades>
            <habilidad>HTML</habilidad>
            <habilidad>CSS</habilidad>
        </habilidades>
    </usuario>
    """
    raiz = ET.fromstring(cadena_xml)
    datos = {raiz.tag: transformar_xml_json(raiz)}
    print(json.dumps(datos, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
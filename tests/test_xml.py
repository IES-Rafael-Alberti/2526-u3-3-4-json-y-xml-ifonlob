import os
import io
import xml.etree.ElementTree as ET
import builtins

import pytest

from src.leer_xml import inicializar_datos, mostrar_datos


@pytest.fixture
def clean_xml_files(tmp_path, monkeypatch):
    """
    Prepara un directorio temporal con cambio de cwd para no tocar tus ficheros reales.
    """
    monkeypatch.chdir(tmp_path)
    yield tmp_path


def test_inicializar_datos_ok(clean_xml_files):
    # Crear datos_usuarios_orig.xml válido
    contenido = """<usuarios>
    <usuario>
        <id>1</id>
        <nombre>Juan</nombre>
        <edad>30</edad>
    </usuario>
    <usuario>
        <id>2</id>
        <nombre>Ana</nombre>
        <edad>25</edad>
    </usuario>
</usuarios>"""
    with open("datos_usuarios_orig.xml", "w", encoding="utf-8") as f:
        f.write(contenido)

    raiz = inicializar_datos()

    # Debe devolver una raíz válida
    assert isinstance(raiz, ET.Element)
    assert raiz.tag == "usuarios"

    # Debe haberse creado el archivo destino
    assert os.path.exists("datos_usuarios.xml")

    # Comprobar que hay 2 usuarios
    usuarios = raiz.findall("usuario")
    assert len(usuarios) == 2


def test_inicializar_datos_origen_no_existe(clean_xml_files, capsys):
    # No crear datos_usuarios_orig.xml
    raiz = inicializar_datos()
    captured = capsys.readouterr()

    assert raiz is None
    assert "no existe. No se realizó la copia" in captured.out


def test_inicializar_datos_xml_invalido(clean_xml_files, capsys):
    # Crear XML mal formado
    with open("datos_usuarios_orig.xml", "w", encoding="utf-8") as f:
        f.write("<usuarios><usuario></usuarios>")  # faltan cierres, etc.

    raiz = inicializar_datos()
    captured = capsys.readouterr()

    assert raiz is None
    assert "formato XML inválido" in captured.out


def test_mostrar_datos_sin_usuarios(capsys):
    # Crear raíz sin usuarios
    raiz = ET.Element("usuarios")

    mostrar_datos(raiz)
    captured = capsys.readouterr()

    assert "ERROR No hay usuarios en el archivo XML." in captured.out


def test_mostrar_datos_con_usuarios(capsys):
    raiz = ET.Element("usuarios")
    u1 = ET.SubElement(raiz, "usuario")
    ET.SubElement(u1, "id").text = "1"
    ET.SubElement(u1, "nombre").text = "Juan"
    ET.SubElement(u1, "edad").text = "30"

    u2 = ET.SubElement(raiz, "usuario")
    ET.SubElement(u2, "id").text = "2"
    ET.SubElement(u2, "nombre").text = "Ana"
    ET.SubElement(u2, "edad").text = "25"

    mostrar_datos(raiz)
    captured = capsys.readouterr()

    assert "ID: 1, Nombre: Juan, Edad: 30" in captured.out
    assert "ID: 2, Nombre: Ana, Edad: 25" in captured.out

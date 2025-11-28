import json
import os

import pytest

from src.leer_json import inicializar_datos, mostrar_datos


@pytest.fixture
def tmp_project_dir(tmp_path, monkeypatch):
    """
    Cambia el directorio de trabajo a uno temporal para no tocar ficheros reales.
    Crea los nombres estándar usados por el programa:
    - datos_usuarios_orig.json
    - datos_usuarios.json
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.mark.parametrize(
    "contenido_origen, espera_none, mensaje_esperado",
    [
        # Caso OK: JSON válido con dos usuarios
        (
            {
                "usuarios": [
                    {"id": 1, "nombre": "Juan", "edad": 30},
                    {"id": 2, "nombre": "Ana", "edad": 25},
                ]
            },
            False,
            "Datos inicializados desde 'datos_usuarios_orig.json' a 'datos_usuarios.json'.",
        ),
        # Caso sin usuarios
        (
            {"usuarios": []},
            True,
            "ERROR. El JSON no contiene usuarios.",
        ),
    ],
)
def test_inicializar_datos_parametrizado(
    tmp_project_dir, contenido_origen, espera_none, mensaje_esperado, capsys
):
    # Crear datos_usuarios_orig.json en el directorio temporal
    with open("datos_usuarios_orig.json", "w", encoding="utf-8") as f:
        json.dump(contenido_origen, f)

    datos = inicializar_datos()
    out = capsys.readouterr().out

    if espera_none:
        assert datos is None
        assert mensaje_esperado in out
        # En este caso no debe crearse un destino válido
        assert not os.path.exists("datos_usuarios.json")
    else:
        assert isinstance(datos, dict)
        assert "usuarios" in datos
        assert os.path.exists("datos_usuarios.json")
        assert mensaje_esperado in out


def test_inicializar_datos_origen_no_existe(tmp_project_dir, capsys):
    # No crear datos_usuarios_orig.json
    datos = inicializar_datos()
    out = capsys.readouterr().out

    assert datos is None
    assert "ERROR El archivo origen 'datos_usuarios_orig.json' no existe. No se realizó la copia." in out
    assert not os.path.exists("datos_usuarios.json")


def test_inicializar_datos_json_invalido(tmp_project_dir, capsys):
    # Crear JSON inválido
    with open("datos_usuarios_orig.json", "w", encoding="utf-8") as f:
        f.write("{usuarios: [}")  # basura

    datos = inicializar_datos()
    out = capsys.readouterr().out

    assert datos is None
    assert "tiene un formato JSON inválido" in out
    assert not os.path.exists("datos_usuarios.json")


@pytest.mark.parametrize(
    "usuarios, mensaje_error",
    [
        ([], "ERROR El archivo JSON no contiene usuarios!"),
        (
            [
                {"id": 1, "nombre": "Juan", "edad": 30},
                {"id": 2, "nombre": "Ana", "edad": 25},
            ],
            None,
        ),
    ],
)
def test_mostrar_datos_parametrizado(usuarios, mensaje_error, capsys):
    datos = {"usuarios": usuarios}

    mostrar_datos(datos)
    out = capsys.readouterr().out

    if mensaje_error:
        assert mensaje_error in out
    else:
        for u in usuarios:
            linea = f"ID: {u['id']}, Nombre: {u['nombre']}, Edad: {u['edad']}"
            assert linea in out

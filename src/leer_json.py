import json

def abrir_json()->dict | str:
    try:
        with open('./datos_usuarios_orig.json','r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return f"Archivo no encontrado"
    except json.JSONDecodeError:
        return "Contenido JSON inválido"
    


def mostrar_datos(resultado:dict):
    print("--- Contenido Actual del JSON ---")
    for usuario in resultado["usuarios"]:
        print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}, Edad: {usuario['edad']}")
    print("--- Fin del Contenido ---")

def inicializar_datos(resulta):


def main():
    resultado = abrir_json()
    if isinstance(resultado,dict) and resultado is not None:
        mostrar_datos(resultado)
    else:
        print(resultado)
        
    
if __name__ == "__main__":
    main()
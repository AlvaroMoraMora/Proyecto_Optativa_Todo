from datetime import datetime
from todo.modelo import GestorTareas, Tarea

def menu() -> None:
    print("=========================================")
    print("        GESTOR DE TARES - CONSOLA        ")
    print("=========================================")
    print("1. Listar tareas")
    print("2. Añadir tarea")
    print("3. Editar tarea")
    print("4. Eliminar tarea")
    print("5. Marcar tarea como completada")
    print("6. Buscar tarea")
    print("7. Filtrar tarea")
    print("8. Guardar y salir")

def listado_tareas() -> None:
    print("+------------------------------------------------------+")
    print("| To-Do List - Usuario                                 |")
    print("+------------------------------------------------------+")

def nueva_tarea() -> dict | None:
    print("-------------- AÑADIR TAREA -------------")
    print("")
    titulo = input("Título: ")
    descripcion = input("Descripcion: ")
    fecha_lim = input("Fecha límite (YYYY-MM-DD) o Enter para saltar: ")
    prioridad = input("Prioridad: ").upper()
    etiquetas = input("Etiquetas: ")

    print("[1] Guardar tarea")
    print("[2] Cancelar")
    opcion = input("Elija una opción: ")

    if opcion == "1":
        tarea = {
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_lim": fecha_lim,
            "prioridad": prioridad,
            "etiquetas": [e.strip() for e in etiquetas.split(",")],
        }

        return tarea

    return None

def


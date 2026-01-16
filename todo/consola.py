from datetime import datetime, date
from todo.modelo import GestorTareas, Tarea, Prioridad


def menu() -> None:
    print("=========================================")
    print("        GESTOR DE TAREAS - CONSOLA       ")
    print("=========================================")
    print("1. Listar tareas")
    print("2. Añadir tarea")
    print("3. Editar tarea")
    print("4. Eliminar tarea")
    print("5. Marcar tarea como completada")
    print("6. Buscar tarea")
    print("7. Filtrar tarea")
    print("8. Guardar y salir")

    opcion = input("Elija una opción: ")

    match opcion:
        case "1":
            listado_tareas()

        case "2":
            nueva_tarea()

        case "3":
            editar_tarea()

        case "4":
            tarea = GestorTareas()

        case "5":
            tarea = GestorTareas()

        case "6":
            tarea = GestorTareas()

        case "7":
            tarea = GestorTareas()

        case "8":
            tarea = GestorTareas()

        case _:
            print("Ha escrito un valor no valido, vuelva a intentarlo")

def listado_tareas(listado = GestorTareas().lista_tareas) -> None:
    print("+------------------------------------------------------+")
    print("| To-Do List - Usuario                                 |")
    print("+---+------------------------------+-------+-----------+")
    print("| # | TÍTULO                       | PRIOR | LÍMITE    |")
    print("+---+------------------------------+-------+-----------+")

    for i, tarea in enumerate(listado, start=1):
        titulo = tarea.titulo
        prioridad = tarea.prioridad.name
        fecha = str(tarea.fecha_limite) if tarea.fecha_limite else ""
        
        print(f"| {i} | {titulo} | {prioridad} | {fecha} |")

    print("+------------------------------------------------------+")

def nueva_tarea() -> None:
    print("-------------- AÑADIR TAREA -------------")
    print("")
    titulo = input("Título: ")
    descripcion = input("Descripcion: ")
    fecha_lim = input("Fecha límite (YYYY-MM-DD) o Enter para saltar: ")
    prioridad = int(input("Prioridad (LOW = 1, MID = 2, HIGH = 3): "))
    etiquetas = input("Etiquetas: ")

    print("[1] Guardar tarea")
    print("[2] Cancelar")
    opcion = input("Elija una opción: ")

    if opcion == "1":
        fecha_lim = date.fromisoformat(fecha_lim) if fecha_lim else None

        tarea = Tarea(titulo, descripcion, fecha_lim, prioridad, etiquetas)

        gestor = GestorTareas()
        gestor.anadir_tarea(tarea)

    return None

def editar_tarea() -> None:
    gestor = GestorTareas()
    listado = gestor.lista_tareas

    print("Elija una tarea a modificar:")

    print("+------------------------------------------------------+")

    for i, tarea in enumerate(listado, start=1):
        titulo = tarea.titulo
        prioridad = tarea.prioridad.name
        fecha = str(tarea.fecha_limite) if tarea.fecha_limite else ""

        print(f"| {i} | {titulo} | {prioridad} | {fecha} |")

    print("+------------------------------------------------------+")

    try:
        i = int(input("Elija una opcion (número): ")) - 1

        if i < 0 or i >= len(gestor.lista_tareas):
            print("Opción inválida.")
            return

        tarea_seleccionada = gestor.lista_tareas[i]
    except ValueError:
        print("Por favor, introduce un número válido.")
        return

    print(f"ID: {tarea_seleccionada.id}")

    print(f"Título: {tarea_seleccionada.titulo}")
    nuevo_titulo = input("Nuevo título: ") or tarea_seleccionada.titulo

    print(f"Descripcion: {tarea_seleccionada.descripcion}")
    nueva_descripcion = input("Nueva descripcion: ") or tarea_seleccionada.descripcion

    print(f"Fecha límite: {tarea_seleccionada.fecha_limite}")
    nuevo_fecha_limite = input("Nueva fecha límite: ")

    if nuevo_fecha_limite:
        try:
            nuevo_fecha_limite = date.fromisoformat(nuevo_fecha_limite)
        except ValueError:
            print("Formato de fecha incorrecto. Se mantendrá la anterior.")
            nuevo_fecha_limite = tarea_seleccionada.fecha_limite
    else:
        nuevo_fecha_limite = tarea_seleccionada.fecha_limite

    print(f"Prioridad: {tarea_seleccionada.prioridad.name}")
    nueva_prioridad = input("Nueva prioridad: ")

    if nueva_prioridad:
        try:
            nueva_prioridad = int(nueva_prioridad)
            nueva_prioridad = Prioridad(nueva_prioridad)
        except (ValueError, KeyError):
            print("Prioridad inválida. Se mantendrá la anterior.")
            nueva_prioridad = tarea_seleccionada.prioridad
    else:
        nueva_prioridad = tarea_seleccionada.prioridad

    print(f"Etiquetas: {tarea_seleccionada.etiquetas}")
    nuevas_etiquetas = input("Nuevas etiquetas: ")

    if nuevas_etiquetas:
        nuevas_etiquetas = [tag.strip() for tag in nuevas_etiquetas.split(',')]
    else:
        nuevas_etiquetas = tarea_seleccionada.etiquetas

    print("[1] Guardar tarea")
    print("[2] Cancelar")
    opcion = input("Elija una opcion: ")

    if opcion == "1":
        nueva_prioridad = nueva_prioridad if nueva_prioridad else tarea_seleccionada.prioridad

        tarea_seleccionada.editar(titulo = nuevo_titulo, descripcion = nueva_descripcion,
            fecha_limite = nuevo_fecha_limite, prioridad = nueva_prioridad, etiquetas = nuevas_etiquetas)

        gestor.guardar()

    return None
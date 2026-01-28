from datetime import datetime, date
from todo.modelo import GestorTareas, Tarea, Prioridad


def menu() -> int:
    print("=========================================")
    print("        GESTOR DE TAREAS - CONSOLA       ")
    print("=========================================")
    print("1. Listar tareas")
    print("2. Añadir tarea")
    print("3. Editar tarea")
    print("4. Eliminar tarea")
    print("5. Marcar/desmarcar tarea como completada")
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
            eliminar_tarea()

        case "5":
            marcar_tarea()

        case "6":
            buscar_tarea()

        case "7":
            filtrar_tarea()

        case "8":
            print("Saliendo del programa...")
            return 1

        case _:
            print("Ha escrito un valor no valido, vuelva a intentarlo")

    return 0

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
    tarea_seleccionada = mostrar_tareas()

    if tarea_seleccionada is None:
        print("No se ha encontrado la tarea seleccionada")
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
    nueva_prioridad = input("Nueva prioridad (LOW = 1, MID = 2, HIGH = 3): ")

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


        gestor.lista_tareas.append(tarea_seleccionada)
        gestor.guardar()

    return None

def eliminar_tarea() -> None:
    gestor = GestorTareas()
    tarea_seleccionada = mostrar_tareas()

    if tarea_seleccionada is None:
        print("No se ha encontrado la tarea seleccionada")
        return

    print("----------- Eliminar tarea -----------")
    print(f"ID: {tarea_seleccionada.id}")
    print(f"Titulo: {tarea_seleccionada.titulo}")

    try:
        opcion = input("¿Seguro que quiere borrar esta tarea? (s/n):")
        opcion = opcion.lower()

        if opcion is None:
            return
    except (ValueError, KeyError):
        print("Ha dado una entrada invalida.")
        return

    if opcion == "s":
        gestor.eliminar(tarea_seleccionada.id)
        return
    if opcion == "n":
        return

def marcar_tarea() -> None:
    tarea_seleccionada = mostrar_tareas()

    if tarea_seleccionada is None:
        print("No se ha encontrado la tarea seleccionada")
        return

    if tarea_seleccionada.completada:
        tarea_seleccionada.desmarcar()
    else:
        tarea_seleccionada.marcar_completada()

    print(f"La tarea: {tarea_seleccionada.titulo} se ha ", "marcado" if tarea_seleccionada.completada else "desmarcado", " correctamente")

def mostrar_tareas() -> Tarea | None:
    gestor = GestorTareas()
    listado = gestor.lista_tareas

    print("Elija una tarea:")

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

        return gestor.lista_tareas[i]
    except (ValueError, KeyError):
        print("Por favor, introduce un valor válido.")
        return


def buscar_tarea() -> None:
    gestor = GestorTareas()
    
    print("-------------- BUSCAR TAREA -------------")
    texto = input("Introduce texto a buscar: ")
    
    if not texto:
        print("Debe introducir un texto de búsqueda.")
        return
    
    resultados = gestor.buscar(texto)
    
    if not resultados:
        print(f"No se encontraron tareas con '{texto}'.")
        return
    
    print(f"\nEncontradas {len(resultados)} tarea(s):\n")
    listado_tareas(resultados)


def filtrar_tarea() -> None:
    gestor = GestorTareas()
    
    print("-------------- FILTRAR TAREAS -------------")
    print("Opciones de filtrado (Enter para saltar):")
    
    estado = input("¿Mostrar completadas (c), pendientes (p), o todas (Enter)? ").lower()
    
    prioridad_input = input("Prioridad (LOW = 1, MID = 2, HIGH = 3) o Enter para todas: ")
    
    etiqueta = input("Buscar por etiqueta: ")
    
    criterios = {}
    
    if estado == 'c':
        criterios['completada'] = True
    elif estado == 'p':
        criterios['completada'] = False
    
    if prioridad_input:
        try:
            criterios['prioridad'] = Prioridad(int(prioridad_input))
        except ValueError:
            print("Prioridad inválida, se ignora este filtro.")
    
    if etiqueta:
        criterios['etiqueta'] = etiqueta
    
    if criterios:
        resultados = gestor.filtrar(**criterios)
    else:
        resultados = gestor.lista_tareas
    
    print("\n¿Ordenar resultados?")
    print("1. Por fecha límite")
    print("2. Por prioridad")
    print("3. Por fecha de creación")
    print("4. Sin ordenar")
    
    orden = input("Elija opción: ")
    
    match orden:
        case "1":
            resultados = sorted(resultados, key=lambda t: (t.fecha_limite is None, t.fecha_limite))
        case "2":
            resultados = sorted(resultados, key=lambda t: t.prioridad.value, reverse=True)
        case "3":
            resultados = sorted(resultados, key=lambda t: t.fecha_creacion)
    
    if not resultados:
        print("No se encontraron tareas con esos criterios.")
        return
    
    print(f"\nEncontradas {len(resultados)} tarea(s):\n")
    listado_tareas(resultados)
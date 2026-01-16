import json
import os
import uuid
from datetime import datetime, date
from enum import IntEnum
from typing import List

"""
Clase Enum que representa el atributo prioridad de la clase Tarea
"""
class Prioridad(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


"""
Clase que representa una tarea individual, encapsulando sus atributos y estado.
"""
class Tarea:
    def __init__(self, titulo, descripcion, fecha_limite, prioridad, etiquetas, id=None, fecha_creacion=None, completada=False):
        self._id = id if id else str(uuid.uuid4())
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_creacion = fecha_creacion if fecha_creacion else datetime.now()
        self._fecha_limite = fecha_limite
        self._prioridad = prioridad
        self._etiquetas = etiquetas
        self._completada = completada

    def marcar_completada(self):
        self.completada = True

    def desmarcar(self):
        self.completada = False

    def editar(self, **kwargs):
        excluidos = ["id", "fecha_creacion"]

        for key, value in kwargs.items():
            if hasattr(self, f"_{key}") or hasattr(self, key):
                if key not in excluidos:
                    setattr(self, key, value)

    def to_dict(self):
        return {
            "id": str(self._id),
            "titulo": self._titulo,
            "descripcion": self._descripcion,
            "fecha_creacion": self._fecha_creacion.isoformat() if isinstance(self._fecha_creacion, (datetime, date)) else self._fecha_creacion,
            "fecha_limite": self._fecha_limite.isoformat() if self.fecha_limite else None,
            "prioridad": self._prioridad,
            "etiquetas": self._etiquetas,
            "completada": self.completada
        }

    @classmethod
    def from_dict(cls, data):
        f_limite = date.fromisoformat(data['fecha_limite']) if data.get('fecha_limite') else None
        f_creacion = datetime.fromisoformat(data['fecha_creacion'])

        return cls(
            titulo=data['titulo'],
            descripcion=data['descripcion'],
            fecha_limite=f_limite,
            prioridad=Prioridad(data['prioridad']),
            etiquetas=data['etiquetas'],
            id=data['id'],
            fecha_creacion=f_creacion,
            completada=data['completada']
        )

    @property
    def id(self) -> str:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def fecha_creacion(self) -> str:
        return self._fecha_creacion

    @property
    def fecha_limite(self) -> str:
        return self._fecha_limite

    @property
    def prioridad(self) -> str:
        return self._prioridad

    @property
    def etiquetas(self) -> list[str]:
        return self._etiquetas

    @property
    def completada(self) -> bool:
        return self._completada

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion

    @fecha_creacion.setter
    def fecha_creacion(self, fecha_creacion):
        self._fecha_creacion = fecha_creacion

    @fecha_limite.setter
    def fecha_limite(self, fecha_limite):
        self._fecha_limite = fecha_limite

    @prioridad.setter
    def prioridad(self, prioridad):
        self._prioridad = prioridad

    @etiquetas.setter
    def etiquetas(self, etiquetas):
        self._etiquetas = etiquetas

    @completada.setter
    def completada(self, completada):
        self._completada = completada


"""
Clase que se encarga del manejo y gestión de los datos de las tareas
"""
class GestorTareas:
    def __init__(self):
        self.ruta_fichero = "data/tareas.json"
        self.lista_tareas = []

        os.makedirs(os.path.dirname(self.ruta_fichero), exist_ok=True)

        self.cargar()


    def anadir_tarea(self, tarea) -> None:
        self.lista_tareas.append(tarea)

    def guardar(self) -> None:
        try:
            lista_para_json = [tarea.to_dict() for tarea in self.lista_tareas]
            with open(self.ruta_fichero, "w") as json_file:
                json.dump(lista_para_json, json_file, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")


    def cargar(self) -> None:
        try:
            with open(self.ruta_fichero, "r") as json_file:
                datos = json.load(json_file)
                self.lista_tareas = [Tarea.from_dict(dato) for dato in datos]
        except FileNotFoundError:
            self.lista_tareas = []
            print("No se ha encontrado el archivo. Se iniciará una lista vacía.")

    def filtrar(self, **criterios) -> None:
        self.lista_tareas = []

    def ordenar(self, key) -> None:
        pass

    """
    Funcion para obtener una tarea según el id
    """
    def obtener_tarea(self, id) -> Tarea | None:
        tarea_filtrada = next((tarea for tarea in self.lista_tareas if tarea.id == id), None)

        if tarea_filtrada is None:
            return None

        return tarea_filtrada

    """
    Funcion para buscar tareas según el titulo o la descripcion
    """
    def buscar(self, texto) -> List[Tarea] | None:
        texto = texto.lower()

        tarea_filtrada = list(filter(lambda tarea: texto in tarea.titulo.lower()
                            or texto in tarea.descripcion.lower(), self.lista_tareas))

        return tarea_filtrada
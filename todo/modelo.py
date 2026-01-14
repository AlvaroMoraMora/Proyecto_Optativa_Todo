import uuid
from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha_limite, prioridad, etiquetas):
        self._id = str(uuid.uuid4())
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_creacion = datetime.now().isoformat()
        self._fecha_limite = fecha_limite
        self._prioridad = prioridad
        self._etiquetas = etiquetas
        self._completada = False

    def marcar_completada(self):
        self.completada = True

    def desmarcar(self):
        self.completada = False

    def editar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        pass

    def from_dict(self):
        pass

    @property
    def id(self) -> str:
        return self.id

    @property
    def titulo(self) -> str:
        return self.titulo

    @property
    def descripcion(self) -> str:
        return self.descripcion

    @property
    def fecha_creacion(self) -> str:
        return self.fecha_creacion

    @property
    def fecha_limite(self) -> str:
        return self.fecha_limite

    @property
    def prioridad(self) -> str:
        return self.prioridad

    @property
    def etiquetas(self) -> list[str]:
        return self.etiquetas

    @property
    def completada(self) -> bool:
        return self.completada

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

class GestorTareas:
    def __init__(self, ruta_fichero, tareas):
        self.ruta_fichero = ruta_fichero
        self.tareas = tareas


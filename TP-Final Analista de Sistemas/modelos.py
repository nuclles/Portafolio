from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List

@dataclass
class Articulo:
    id_articulo: str
    codigo: str
    descripcion: str

@dataclass
class Recurso:
    id_recurso: str
    nombre: str
    tipo: str  # e.g., 'MAQUINA', 'HM'

@dataclass
class Operario:
    id_operario: str
    nombre: str
    legajo: str

@dataclass
class TiemposElemento:
    elemento: str
    valoracion: float
    minutos: float
    segundos: float
    elementos_medidos: int = 1
    lote_frecuencial: float = 1.0
    suplemento: float = 0.0

@dataclass
class Relevamiento:
    id_relevamiento: Optional[str] = None
    id_tarea: Optional[int] = None
    articulo: Optional[Articulo] = None
    operacion: str = ""
    recurso: Optional[Recurso] = None
    hm: Optional[Recurso] = None
    operario: Optional[Operario] = None
    fecha: date = field(default_factory=date.today)
    postura: str = "pie"  # pie o sentado
    piezas_por_golpe: int = 1
    articulos_por_golpe: int = 1
    operarios_maquina: int = 1
    tiempos: List[TiemposElemento] = field(default_factory=list)

@dataclass
class Informe:
    id_informe: Optional[str] = None
    relevamiento: Optional[Relevamiento] = None
    tiempo_estandar_op: float = 0.0
    cadencia_ph: float = 0.0
    cadencia_h1000: float = 0.0
    estandar_epicor: float = 0.0
    dotacion_epicor: int = 1

@dataclass
class Usuario:
    """
    Representa un usuario del sistema para autenticación y RBAC.
    """
    id_usuario: int
    username: str
    password_hash: str
    rol: str  # "METODISTA" o "JEFE/GERENTE"
    nombre: str

@dataclass
class Tarea:
    """
    Representa una tarea o solicitud de relevamiento a mostrar en el Dashboard.
    """
    id_tarea: int
    titulo: str
    descripcion: str
    estado: str  # "Pendiente", "En Proceso", "Completado", "Finalizado", "Cerrado"
    fecha: str
    informe_url: str
    id_usuario_asignado: Optional[int] = None

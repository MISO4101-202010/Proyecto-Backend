from enum import IntEnum


class TipoActividadEnum(IntEnum):
    """
    Enum con los tipos de pregunta disponibles dentro del sistema.
    """
    SELECCION_MULTIPLE = 1,
    VERDADERO_O_FALSO = 2,
    ABIERTA = 3,
    PAUSA = 4

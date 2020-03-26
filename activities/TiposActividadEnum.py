from enum import IntEnum


class TipoActividadEnum(IntEnum):
    '''
    Enum con los tipos de pregunta disponibles dentro del sistema.
    '''
    SELECCION_MULTIPLE = 1,
    FALSO_O_VERDADERO = 2,
    ABIERTA = 3

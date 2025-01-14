from enum import Enum, auto

class STATUS(Enum):
    pass

class LEAKAGE_MODEL(Enum):
    HAMMING_WEIGHT = auto()
    HAMMING_DISTANCE = auto()

class TARGET:
    class AES(Enum):
        FIRST_ROUND = auto()
        LAST_ROUND = auto()
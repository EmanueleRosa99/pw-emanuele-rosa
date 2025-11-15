from abc import ABC, abstractmethod
from typing import Tuple


# Classe astratta prodotto
class Prodotto(ABC):
    
    def __init__(self):
        self._nome = self.__class__.__name__
    
    @property
    def nome(self) -> str:
        return self._nome
    
    # Range di tempo di produzione del singolo prodotto
    @property
    @abstractmethod
    def range_tempo_produzione(self) -> Tuple[float, float]:
        pass
    
     # Range di quantità da produrre di prodotto
    @property
    @abstractmethod
    def range_quantita_produzione(self) -> Tuple[int, int]:
        pass
    
    @property
    @abstractmethod
    def nome(self) -> str:
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
    
    def __str__(self) -> str:
        return self.nome


class GiaccaInvernale(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (3.5, 8.0)
    
    @property
    def range_quantita_produzione(self) -> Tuple[int, int]:
        return (30, 120)
    
    @property
    def nome(self) -> str:
        return "Giacche Invernali"


class TShirt(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (0.5, 1.8)
    
    @property
    def range_quantita_produzione(self) -> Tuple[int, int]:
        return (100, 250)
    
    @property
    def nome(self) -> str:
        return "T-Shirts"


class Felpa(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (1.5, 4.0)
    
    @property
    def range_quantita_produzione(self) -> Tuple[int, int]:
        return (65, 190)
    
    @property
    def nome(self) -> str:
        return "Felpe"


class Pantalone(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (1.8, 4.5)
    
    @property
    def range_quantita_produzione(self) -> Tuple[int, int]:
        return (50, 170)
    
    @property
    def nome(self) -> str:
        return "Pantaloni"


class LineaProduttiva:
    
    def __init__(self, nome: str, coefficiente_efficienza: float):
        self.nome = nome
        self.coefficiente_efficienza = coefficiente_efficienza
    
    def calcola_capacita_giornaliera(self, tempo_per_unita: float, ore_giornaliere: int = 24) -> int:
        capacita = (ore_giornaliere * self.coefficiente_efficienza) / tempo_per_unita
        return int(capacita)
    
    def __repr__(self) -> str:
        return f"<Linea {self.nome}: efficienza {self.coefficiente_efficienza:.2f}>"
    
    def __str__(self) -> str:
        return f"Linea {self.nome} (efficienza: {self.coefficiente_efficienza:.2f})"


class Impianto:
    
    def __init__(self, linee: list[LineaProduttiva]):
        self.linee = linee
    
    @property
    def numero_linee(self) -> int:
        return len(self.linee)
    
    def __repr__(self) -> str:
        return f"<Impianto: {self.numero_linee} linee>"

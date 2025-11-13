from abc import ABC, abstractmethod
from typing import Tuple

#Classe astratta prodotto, da cui ereditano le sottoclassi specifiche per tipologia
class Prodotto(ABC):
    
    def __init__(self):
        self._nome = self.__class__.__name__
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    @abstractmethod
    def range_tempo_produzione(self) -> Tuple[float, float]:
        pass
    
    @property
    @abstractmethod
    def range_capacita_giornaliera(self) -> Tuple[int, int]:
        pass
    
    @property
    def nome(self) -> str:
        """Nome visualizzato del prodotto."""
        return self._nome
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
    
    def __str__(self) -> str:
        return self.nome


class GiaccaInvernale(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (3.5, 8.0)
    
    @property
    def range_capacita_giornaliera(self) -> Tuple[int, int]:
        return (8, 15)
    
    @property
    def nome(self) -> str:
        return "Giacche Invernali"


class TShirt(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (0.5, 1.8)
    
    @property
    def range_capacita_giornaliera(self) -> Tuple[int, int]:
        return (80, 120)
    
    @property
    def nome(self) -> str:
        return "T-Shirts"


class Felpa(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (1.5, 4.0)
    
    @property
    def range_capacita_giornaliera(self) -> Tuple[int, int]:
        return (30, 50)
    
    @property
    def nome(self) -> str:
        return "Felpe"


class Pantalone(Prodotto):
    
    @property
    def range_tempo_produzione(self) -> Tuple[float, float]:
        return (1.8, 4.5)
    
    @property
    def range_capacita_giornaliera(self) -> Tuple[int, int]:
        return (25, 45)
    
    @property
    def nome(self) -> str:
        return "Pantaloni"


class Impianto:
    
    def __init__(self, linee: list[Tuple[str, float]]):
        self.linee = linee
    
    @property
    def capacita_totale(self) -> float:
        return sum(cap for _, cap in self.linee)
    
    @property
    def numero_linee(self) -> int:
        return len(self.linee)
    
    def __repr__(self) -> str:
        return f"<Impianto: {self.numero_linee} linee, capacità {self.capacita_totale:.2f}>"

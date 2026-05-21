from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class Cycle(Enum):
    PRIMAIRE = "Primaire"
    COLLEGE = "Collège"
    LYCEE = "Lycée"
    UNIVERSITE = "Université"


@dataclass
class Eleve:
    id: Optional[int] = None
    nom: str
    prenom: str
    date_naissance: date
    email: str
    telephone: str
    adresse: str
    classe: str
    matricule: str
    cycle: Cycle
    situation_financiere: str
    date_inscription: datetime = field(default_factory=datetime.now)

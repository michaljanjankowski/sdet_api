import os
import requests
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import List, Optional


@dataclass
class Characteristis:
    prey: Optional[str] = None
    name_of_young: Optional[str] = None
    group_behavior: Optional[str] = None
    estimated_population_size: Optional[str] = None
    biggest_threat: Optional[str] = None
    most_distinctive_feature: Optional[str] = None
    gestation_period: Optional[str] = None
    habitat: Optional[str] = None
    predators: Optional[str] = None
    diet: Optional[str] = None
    average_litter_size: Optional[str] = None
    lifestyle: Optional[str] = None
    common_name: Optional[str] = None
    number_of_species: Optional[str] = None
    location: Optional[str] = None
    slogan: Optional[str] = None
    group: Optional[str] = None
    color: Optional[str] = None
    skin_type: Optional[str] = None
    top_speed: Optional[str] = None
    lifespan: Optional[str] = None
    weight: Optional[str] = None
    length: Optional[str] = None
    age_of_sexual_maturity: Optional[str] = None
    age_of_weaning: Optional[str] = None


@dataclass
class Taxonomy:
    kingdom: Optional[str] = None
    phylum: Optional[str] = None
    order: Optional[str] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    scientific_name: Optional[str] = None


@dataclass
class AnimalResponse(JSONWizard):
    name: str
    taxonomy : Taxonomy
    locations : List[str]
    characteristics: Characteristis

class API_Service:
    def __init__(self, api_key: str | None = None, session: requests.Session | None = None) -> None:
        self.api_key = api_key or os.getenv("API_ANIMALS_KEY")
        if not self.api_key:
            raise ValueError("API_ANIMALS_KEY is required")
        self.session = session or requests.Session()
        self.calls_history: list[list[AnimalResponse]] = []

    def get_animal(self, name: str) -> list[AnimalResponse]:
        response = self.session.get(
            "https://api.api-ninjas.com/v1/animals",
            params={"name": name},
            headers={"X-Api-Key": self.api_key},
            timeout=5,
        )
        response.raise_for_status()
        animals = [AnimalResponse.from_dict(item) for item in response.json()]
        self.calls_history.append(animals)
        return animals

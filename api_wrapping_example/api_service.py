import os
import requests
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from typing import Dict, List, Optional


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

class API_Service():
    api_key = os.getenv("API_ANIMALS_KEY")
    last_success_response = None
    last_failed_response = None
    calls_history = []

    def get_animal(self, name):
        api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(name)
        last_response = requests.get(api_url, headers={'X-Api-Key':self.api_key})
        if last_response.status_code == requests.codes.ok:
            self.last_success_response = AnimalResponse.from_json(last_response.text)
            self.calls_history.append(self.last_success_response)
        else:
            self.last_failed_response = last_response
            self.calls_history.append(self.last_failed_response)


if __name__ == "__main__":
    api_serv = API_Service()
    api_serv.get_animal(name="cat")
    assert  api_serv.last_success_response
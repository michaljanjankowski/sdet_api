import json
import dataclasses
from api_service import API_Service

class API_Wrapper(API_Service):

    @staticmethod
    def show_few_characteristic(positive_response):
        name_charteristics_to_show = {}
        for idx, animal in enumerate(positive_response):
            if idx == 4:
                break
            name_charteristics_to_show[animal.name]=json.dumps(dataclasses.asdict(animal.characteristics,
                                                dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        print(f"Few characteristis: {name_charteristics_to_show}")

    def start(self):
        while True:
            animal_name = input("Please enter animal name: ")
            if animal_name == '':
                print("Enter pressed")
                break
            self.get_animal(name=animal_name)
            animals_names = [animal.name for animal in self.last_success_response]
            print(f"I have found the following animals: {animals_names}")
            API_Wrapper.show_few_characteristic(self.last_success_response)

if __name__ == "__main__":
    api_wrapper = API_Wrapper()
    api_wrapper.start()



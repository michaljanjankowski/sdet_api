"""Small presentation layer for the animal API example."""

import argparse
import dataclasses

from api_wrapping_example.api_service import API_Service, AnimalResponse


def summarize_animals(animals: list[AnimalResponse], limit: int = 4) -> dict[str, dict]:
    return {
        animal.name: {
            key: value
            for key, value in dataclasses.asdict(animal.characteristics).items()
            if value is not None
        }
        for animal in animals[:limit]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the API Ninjas animals endpoint")
    parser.add_argument("name", help="Animal name to search for")
    args = parser.parse_args()
    print(summarize_animals(API_Service().get_animal(args.name)))


if __name__ == "__main__":
    main()

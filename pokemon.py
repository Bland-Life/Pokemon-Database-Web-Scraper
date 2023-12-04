from dataclasses import dataclass

@dataclass
class Pokemon():
    id: int = None
    name: str = None
    species: str = None
    types: list[str] = None
    height: str = None
    weight: str = None
    abilities: dict = None
    evolutions: list = None
    entry_info: str = None
    img_ref: str = None
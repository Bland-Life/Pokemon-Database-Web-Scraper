import pokedex as pdx
import json


def pokdex_json(pokedex: dict):
    with open('pokemondb.json', 'w', encoding='utf-8') as file:
        json_obj = json.dumps(pokedex, indent=4)
        file.write(json_obj)


def pokdex_csv(pokedex: dict):
    pass


def pokdex_sql(pokedex: dict):
    pass


raw_links = pdx.scrape_pokedex()

# Removes Duplicate Links
links = []
[links.append(link) for link in raw_links if link not in links]

pokemons = []
total = len(links)
for i, link in enumerate(links[:3]):
    pokemons.append(pdx.scrape_entry(link))
    print(f"{i + 1}/{total} Completed")

pokemon_dict = {
    "pokemons": pokemons
}

print(pokemon_dict)
pokdex_json(pokemon_dict)

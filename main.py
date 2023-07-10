import pokedex as pdx
import json, csv


def pokedex_json(pokedex: dict):
    with open('pokedex.json', 'w', encoding='utf-8') as file:
        json_obj = json.dumps(pokedex, indent=4)
        file.write(json_obj)


def pokedex_csv(pokedex: list):
    headers = list(pokedex[0].keys())
    with open('pokedex.csv', mode='w', encoding='UTF8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(pokedex)

raw_links = pdx.scrape_pokedex()

# Removes Duplicate Links
links = []
[links.append(link) for link in raw_links if link not in links]

pokemons = []
total = len(links)
for i, link in enumerate(links):
    pokemons.append(pdx.scrape_entry(link))
    print(f"{i + 1}/{total} Completed")

'''
# TO SAVE DATA AS A JSON

pokemon_dict = {
    "pokemons": pokemons
}

pokedex_json(pokemon_dict)


# TO SAVE DATA AS A CSV

pokedex_csv(pokemons)
'''


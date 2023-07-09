import pokedex as pdx
import json

raw_links = pdx.scrape_pokedex()

# Removes Duplicate Links
links = []
[links.append(link) for link in raw_links if link not in links]


list_length = len(links)

# Appends the dictionary entries to the list and keep track of progress
for i, link in enumerate(links):

    pdx.pokemons.append(pdx.scrape_entry(link))
    print(f"{i + 1}/{list_length} Completed")

pokemon_dict = {
    'data': pdx.pokemons
}

with open('pokemondb.json', 'w') as file:
    json_obj = json.dumps(pokemon_dict, indent=4)
    file.write(json_obj)

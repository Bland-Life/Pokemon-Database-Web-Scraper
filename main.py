import requests
import json

from bs4 import BeautifulSoup

pokemon_db = 'https://pokemondb.net'
pokemons = []


def scrape_pokedex():
    '''Scrapes the pokemondb site for the links to every pokemon entry, it will return all those links in a list best used with the scrape_entry function'''
    link = f"{pokemon_db}/pokedex/all"
    response = requests.get(url=link)
    response.encoding = 'utf-8'
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')
    return [link['href'] for link in soup.select(".ent-name")]


def scrape_entry(link):
    '''Takes a link to a pokedex entry page, such as https://pokemondb.net/pokedex/bulbasaur. The information that is obtained from the page will
    be added to a dictionary which will be returned.'''
    
    pokedex_entry = f'{pokemon_db}{link}'

    response = requests.get(url=pokedex_entry)
    response.encoding = 'utf-8'
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')
    pokemon_name = None
    id = None
    species = None
    types = None
    height = None
    weight = None
    abilities = None
    evolutions = None
    entry_info = None
    img = None
    
    pokemon_name = soup.find('h1').text
    img = soup.select_one('main picture img')['src']


    # Scans each row within the table that contains most of the pokemon data.
    table = soup.select_one('.vitals-table')
    rows = table.find_all('tr')
    for row in rows:
        if row.find('th').text == 'Type':
            types = [type.text for type in row.find_all('a')]

        if row.find('th').text == 'Species':
            species = row.find('td').text

        if row.find('th').text == 'Weight':
            weight = row.find('td').text
        
        if row.find('th').text == 'Height':
            height = row.find('td').text

        if row.find('th').text == 'Abilities':
            abilities = [type.text for type in row.find_all('a')]

        if row.find('th').text == 'National №':
            id = row.find('td').text
    
    evolutions = [link.text for link in soup.select('#dex-evolution + h2 + div .ent-name')]
    entry_info = soup.select_one('#dex-flavor + h2 + div td')
    
    # If there isn't an entry stored, some pages have a slightly altered format
    if not entry_info:
        entry_info = soup.select_one('#dex-flavor + h2 + h3 + div td')

    # If there STILL isn't an entry stored, there probably isn't one on the page
    if not entry_info:
        entry_info = 'No Entry'
    else:
        entry_info = entry_info.text

    new_entry = {
        'id': id,
        'name': pokemon_name,
        'species': species,
        'types': types,
        'height': height,
        'weight': weight,
        'abilities': abilities,
        'evolutions': evolutions,
        'facts': entry_info,
        'site_link': pokedex_entry,
        'img_link': img
    }
    return new_entry


# ----------------------
# ---------------------- CODE STARTS HERE 
# ----------------------
raw_links = scrape_pokedex()

# Removes Duplicate Links
links = []
[links.append(link) for link in raw_links if link not in links]


list_length = len(links)

# Appends the dictionary entries to the list and keep track of progress
for i, link in enumerate(links):

    pokemons.append(scrape_entry(link))
    print(f"{i + 1}/{list_length} Completed")

pokemon_dict = {
    'data': pokemons
}

with open('pokemondb.json', 'w') as file:
    json_obj = json.dumps(pokemon_dict, indent=4)
    file.write(json_obj)

import requests, time
from bs4 import BeautifulSoup

pokemon_db = 'https://pokemondb.net'
CRAWL_DELAY = 4


def scrape_pokedex() -> list[str]:
    """
    Scrapes the pokemondb site for the routes to every pokemon entry, it will return all those routes in a list.
    """

    pokemon: str = input('Enter a Pokemon name or ID (leave empty to scrape all): ')
    
    if pokemon:
        pokemon = pokemon.replace(" ", "-").replace(".", "")
        return [f'/pokedex/{pokemon}']
    
    link = f"{pokemon_db}/pokedex/all"
    response = requests.get(url=link)
    time.sleep(CRAWL_DELAY)
    webpage = response.text
    soup = BeautifulSoup(webpage, 'html.parser')
    return [link['href'] for link in soup.select(".ent-name")]


def scrape_entry(link: str):
    """
    Takes a route to a pokedex entry page and scrapes for basic information.

    It uses the routes obtained from the scrape_pokedex method e.g. '/pokedex/bulbasaur' and will combine it with the main site link to request the web page.
    Afterwards, it will obtain basic information like the pokemon name, typing, evolution, etc. and return it in a dictionary.
    """
    
    pokedex_entry = f'{pokemon_db}{link}'

    response = requests.get(url=pokedex_entry)
    time.sleep(CRAWL_DELAY)
    webpage = response.text
    soup = BeautifulSoup(webpage.encode('utf-8'), 'html.parser')

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


    # The first table found contains most of the data, so this is just scanning each row of that table.
    table = soup.select_one('.vitals-table')
    rows = table.find_all('tr')
    for row in rows:
        if row.find('th').text == 'National №':
            id = row.find('td').text
        
        if row.find('th').text == 'Species':
            species = row.find('td').text

        if row.find('th').text == 'Type':
            types = [type.text for type in row.find_all('a')]
        
        if row.find('th').text == 'Height':
            height = row.find('td').text.replace(u'\xa0', u' ')

        if row.find('th').text == 'Weight':
            weight = row.find('td').text.replace(u'\xa0', u' ')
        
        if row.find('th').text == 'Abilities':
            abilities = {
                'normal': [type.text[3:] for type in row.find_all('span')],
                'hidden':  [type.text.replace(' (hidden ability)', '') for type in row.find_all('small')]
            }
    
    evolution_paths = soup.find_all(class_='infocard-list-evo')
    evolutions: list = []
    for path in evolution_paths:
        evolutions.extend(link.text for link in path.select(f'.ent-name') if link.text not in evolutions)

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
        'id': int(id),
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
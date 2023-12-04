import requests, time
from bs4 import BeautifulSoup
from pokemon import Pokemon

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
    pokemon = Pokemon()

    pokemon.name = soup.find('h1').text
    pokemon.img_ref = soup.select_one('main picture img')['src']


    # The first table found contains most of the data, so this is just scanning each row of that table.
    table = soup.select_one('.vitals-table')
    rows = table.find_all('tr')
    for row in rows:
        if row.find('th').text == 'National №':
            pokemon.id = row.find('td').text
        
        if row.find('th').text == 'Species':
            pokemon.species = row.find('td').text

        if row.find('th').text == 'Type':
            pokemon.types = [type.text for type in row.find_all('a')]
        
        if row.find('th').text == 'Height':
            pokemon.height = row.find('td').text.replace(u'\xa0', u' ')

        if row.find('th').text == 'Weight':
            pokemon.weight = row.find('td').text.replace(u'\xa0', u' ')
        
        if row.find('th').text == 'Abilities':
            pokemon.abilities = {
                'normal': [type.text[3:] for type in row.find_all('span')],
                'hidden':  [type.text.replace(' (hidden ability)', '') for type in row.find_all('small')]
            }
    
    evolution_paths = soup.find_all(class_='infocard-list-evo')
    pokemon.evolutions: list = []
    for path in evolution_paths:
        pokemon.evolutions.extend(link.text for link in path.select(f'.ent-name') if link.text not in pokemon.evolutions)

    pokemon.entry_info = soup.select_one('#dex-flavor + h2 + div td')

    # If there isn't an entry stored, some pages have a slightly altered format
    if not pokemon.entry_info:
        pokemon.entry_info = soup.select_one('#dex-flavor + h2 + h3 + div td')

    # If there STILL isn't an entry stored, there probably isn't one on the page
    if not pokemon.entry_info:
        pokemon.entry_info = 'No Entry'
    else:
        pokemon.entry_info = pokemon.entry_info.text

    return pokemon.__dict__
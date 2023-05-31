from requests import get, exceptions
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pokemondb.net/pokedex/all"

try:
    response = get(url)
    response.raise_for_status()
    print("Success")
    
except exceptions.RequestException as error:
    print(f'Requisition Error | {error}')
    
except exceptions.HTTPError as error:
    print(f'HTTP Error| {error}')
    
except exceptions.ConnectionError as error:
    print(f'Connecetion Error | {error}')
    
except Exception as error:
    print(f'An unexpected error occurred | {error}')
    
soup = BeautifulSoup(response.content, 'html.parser')
pokedex_table = soup.find('table', id='pokedex').find_all('tr')

pokedex_stats = {
                'Pokemon Id': [],
                'Name': [],
                'Types': [],
                'Total': [],
                'Hp': [],
                'Attack': [],
                'Defense': [],
                'Speed Attack': [],
                'Speed Defense': [],
                'Speed': [],
                }

def colect_pokemon_stats(pokedex_stats, number):
    pokemon_info = pokedex_table[number].find_all('td')
    stats_keys = list(pokedex_stats.keys())
    for i, key in enumerate(stats_keys):
        pokedex_stats[key].append(pokemon_info[i].get_text())

def extract_pokemon_stats(data_source):
    total_pokemons = len(data_source)
    for pokemon in range(1, total_pokemons):
        colect_pokemon_stats(pokedex_stats, pokemon)
        
extract_pokemon_stats(pokedex_table)
pokedex_data = pd.DataFrame(pokedex_stats)
pokedex_data.to_csv('pokedex_data_v1.csv', sep=',',  index=False)

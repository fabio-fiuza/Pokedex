from requests import get, exceptions
from bs4 import BeautifulSoup
import pandas as pd
from typing import List


url = "https://pokemondb.net/pokedex/all"

try:
    response = get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    pokedex_table = soup.find('table', id='pokedex').find_all('tr')

except exceptions.RequestException as error:
    print(f'Requisition Error | {error}')

except exceptions.HTTPError as error:
    print(f'HTTP Error | {error}')

except exceptions.ConnectionError as error:
    print(f'Connection Error | {error}')

except Exception as error:
    print(f'An unexpected error occurred | {error}')


def extract_pokemon_stats(data_source: List[BeautifulSoup]) -> pd.DataFrame:
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

    for pokemon_info in data_source[1:]:
        
        stats: List[str] = [tag.get_text() for tag in pokemon_info.find_all('td')]

        for key, value in zip(pokedex_stats.keys(), stats):
            pokedex_stats[key].append(value)

    return pd.DataFrame(pokedex_stats)


pokedex_data = extract_pokemon_stats(pokedex_table)
pokedex_data.to_csv('pokedex_data_v1.csv', sep=',', index=False)
import requests

def extract_ability():
    pages = []
    for num in range(0,4):
        url = f'https://pokeapi.co/api/v2/ability/?offset={num*100}&limit=100'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pages.append(data)
        else:
            raise Exception('ABILITY API ERROR')
    
    return pages

def extract_type():
    url = 'https://pokeapi.co/api/v2/type/?offset=0&limit=21'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('TYPE API ERROR')

def extract_pokemon():
    pages = []
    for num in range(0,27):
        url = f'https://pokeapi.co/api/v2/pokemon?offset={num*50}&limit=50'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pages.append(data)
        else:
            raise Exception('POKEMON API ERROR')
    
    return pages

def extract_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('API ERROR')
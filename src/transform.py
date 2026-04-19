import pandas as pd
from extract import extract_data

def transform_ability(data):
    data2 = data[0]['results']
    for i in range(1, len(data)):
        data2 = data2 + data[i]['results']
    list = []

    for ability in data2:
        name = ability['name']

        list.append({
            'name': name
        })
    
    return pd.DataFrame(list)

def transform_type(data):
    list = []

    for type in data['results']:
        name = type['name']

        list.append({
            'name': name
    })
    
    return pd.DataFrame(list)

def transform_poke(data):
    data2 = data[0]['results']
    for i in range(1, len(data)):
        data2 = data2 + data[i]['results']
    list = []

    for i, pokemon in enumerate(data2):
        unique = extract_data(data2[i]['url'])
        id = unique['id']
        name = pokemon['name']
        weight = unique['weight']
        height = unique['height']
        types = [unique['types'][0]['type']['name']]
        ability = None
        
        if len(unique['types']) > 1:
            types.append(unique['types'][1]['type']['name'])
        if unique['abilities']:
            ability = unique['abilities'][0]['ability']['name']

        list.append({
            'id': id,
            'name': name,
            'weight': weight,
            'height': height,
            'types': types,
            'ability': ability
        })

    return pd.DataFrame(list)
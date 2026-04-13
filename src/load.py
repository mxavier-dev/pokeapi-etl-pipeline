from connect.connection import connect
import json
from datetime import datetime

def save_raw(table, data):
    time = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    filename = f'data/raw/{table}_raw_{time}.json'
    with open(filename, 'w', encoding='utf-8') as arq:
        json.dump(data, arq, indent=4)

def save_processed(table, data):
    time = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    filename = f'data/processed/{table}_processed_{time}.json'
    if type(data) == dict:
        with open(filename, 'w', encoding='utf-8') as arq:
            json.dump(data, arq, indent=4)
    else:
        data.to_json(filename, orient='records', indent=4, force_ascii=False)

def insert_type(cursor, pokemon_id, type_ids):

    values_types = [(pokemon_id, t_id) for t_id in type_ids]

    cursor.executemany("""
        INSERT IGNORE INTO pokemon_types (pokemon_id, type_id)
        VALUES (%s, %s)
    """, values_types)

def insert_ability(cursor, pokemon_id, abilities_ids):

    values_abilities = [(pokemon_id, a_id) for a_id in abilities_ids]

    cursor.executemany("""
        INSERT IGNORE INTO pokemon_abilities (pokemon_id, ability_id)
        VALUES (%s, %s)
    """, values_abilities)

def insert_pokemon(cursor, data):
    name = data['name']
    weight = data['weight']
    height = data['height']

    query = """
    INSERT INTO pokemon (name, weight, height)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    name = VALUES(name)
    """
    values = (name,weight,height,)

    cursor.execute(query, values)

def get_or_create_type(cursor, type_name):

    query = """INSERT INTO types (name)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE
            id = LAST_INSERT_ID(id)"""

    cursor.execute(query, (type_name,))

    return cursor.lastrowid


def get_or_create_ability(cursor, ability_name):

    query = """INSERT INTO abilities (name)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE
            id = LAST_INSERT_ID(id)"""
    
    cursor.execute(query, (ability_name,))

    return cursor.lastrowid

def insert_all(data):

    conn = connect()
    cursor = conn.cursor()
    print()

    try:
        values = [
            (int(row["id"]), row["name"], row["weight"], row["height"])
            for _, row in data.iterrows()
            ]
        cursor.executemany("""INSERT INTO pokemon (id, name, weight, height)
                           VALUES (%s,%s,%s,%s)
                           ON DUPLICATE KEY UPDATE
                           name = VALUES(name)""", values)
        
        all_types = set(t for types in data['types'] for t in types)
        cursor.executemany("""INSERT IGNORE INTO types (name)
                           VALUES (%s)
                           """, [(t,) for t in all_types])
        
        all_abilities = set(a for ability in data['ability'] for a in ability)

        cursor.executemany("""INSERT IGNORE INTO abilities (name)
                           VALUES (%s)
                           """, [(a,) for a in all_abilities])

        cursor.execute("SELECT id, name FROM types")
        type_map = {name: id for id, name in cursor.fetchall()}

        df_exploded = data.explode("types")

        values = list(
            zip(
                df_exploded["id"].astype(int),
                df_exploded["types"].map(type_map)
            ))
        cursor.executemany("""
                           INSERT IGNORE INTO pokemon_types
                           (pokemon_id, type_id)
                           VALUES (%s, %s)
                           """, values)
        
        df_exploded = data.explode("ability")

        values = list(
            zip(
                df_exploded["id"].astype(int),
                df_exploded["types"].map(type_map)
            ))
        cursor.executemany("""
                           INSERT IGNORE INTO pokemon_types
                           (pokemon_id, type_id)
                           VALUES (%s, %s)
                           """, values)


        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()
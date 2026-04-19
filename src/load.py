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

def insert_all(data):

    conn = connect()
    cursor = conn.cursor()

    try:
        values = [
            (int(row["id"]), row["name"], row["weight"], row["height"])
            for _, row in data.iterrows()
        ]
        cursor.executemany("""INSERT INTO pokemon (id, name, weight, height)
                           VALUES (%s,%s,%s,%s)
                           ON DUPLICATE KEY UPDATE
                           name = VALUES(name)""", values)

        all_types = set(t for types in data["types"] for t in types)
        cursor.executemany("""INSERT IGNORE INTO types (name)
                           VALUES (%s)""", [(t,) for t in all_types])

        all_abilities = set(data["ability"].dropna().unique())
        cursor.executemany("""INSERT IGNORE INTO abilities (name)
                           VALUES (%s)""", [(a,) for a in all_abilities])

        cursor.execute("SELECT id, name FROM types")
        type_map = {name: id for id, name in cursor.fetchall()}

        cursor.execute("SELECT id, name FROM abilities")
        ability_map = {name: id for id, name in cursor.fetchall()}

        df_types = data.explode("types")
        values = [
            (int(row["id"]), type_map[row["types"]])
            for _, row in df_types.iterrows()
        ]
        cursor.executemany("""
                           INSERT IGNORE INTO pokemon_types
                           (pokemon_id, type_id)
                           VALUES (%s, %s)
                           """, values)

        ability_rows = [
            (int(row["id"]), ability_map[row["ability"]])
            for _, row in data.dropna(subset=["ability"]).iterrows()
        ]
        if ability_rows:
            cursor.executemany("""
                               INSERT IGNORE INTO pokemon_abilities
                               (pokemon_id, ability_id)
                               VALUES (%s, %s)
                               """, ability_rows)

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()
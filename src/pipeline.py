from extract import extract_pokemon, extract_ability, extract_type
from transform import transform_ability, transform_poke, transform_type, concat_df
from load import insert_all, save_processed, save_raw
from utils.logger import get_logger

logger = get_logger()

logger.info('--- Starting Pipeline ---')
def pipeline():
    try:
        logger.info('Starting extraction')
        data_ability = extract_ability()
        data_pokemon = extract_pokemon()
        data_type = extract_type()

        logger.info('Saving raw data')
        # save_raw('pokemon', data_pokemon) 
        # save_raw('ability', data_ability)
        # save_raw('type', data_type)

        logger.info('Transforming data')
        df_a = transform_ability(data_ability)
        df_p = transform_poke(data_pokemon)
        df_t = transform_type(data_type)

        logger.info('Saving transformed data')
        # save_processed('ability', df_a)
        # save_processed('type', df_t)
        # save_processed('pokemon', df_p)
        
        logger.info('Loading data to the database')
        insert_all(df_p)

        logger.info('Pipeline completed successfully')
    except Exception as e:
        logger.error(f'Pipeline error: {e}')
        raise

if __name__ == '__main__':
    pipeline()
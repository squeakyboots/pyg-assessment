"""Crypto Interview Assessment Module."""

import os
from dotenv import find_dotenv, load_dotenv
import crypto_api
from mysql.connector import connect, Error
import logging
from logging.handlers import TimedRotatingFileHandler
from sys import stdout

console_handler = logging.StreamHandler(stdout)
timed_rotate_handler = TimedRotatingFileHandler('storage/app.log', when='D', interval=7, backupCount=2)
logger = logging.getLogger("Rotating Log")

load_dotenv(find_dotenv(raise_error_if_not_found=True))

DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_PORT = os.getenv("DB_PORT")


def top_three_by_market_cap():
    """Get the top 3 cryptocurrency coins' ID, symbol, name, current price, and market cap based on current market cap.

    :return: Top three cryptocurrency coins by current market cap.
    :rtype: tuple
    """
    try:
        coins = crypto_api.get_coins()[:3]
    except Exception as err:
        logger.critical(f'Error getting top three coins via API: {err}')
        return ()
    return tuple(coins)


def write_to_db(coins):
    """Write a tuple of cryptocurrency coins to the database.

    :param coins: Coins pulled from coingecko's API
    :type coins: tuple[dict]
    :rtype: None
    """
    try:
        with connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD,
                     database=DB_DATABASE) as connection:
            query = """
                INSERT INTO Coin 
                (CoinID, CoinSymbol, CoinName, CoinCurrentPrice, CoinMarketCap) 
                VALUES ( %s, %s, %s, %s, %s ) 
                ON DUPLICATE KEY UPDATE CoinID=VALUES(CoinID), CoinSymbol=VALUES(CoinSymbol), CoinName=VALUES(CoinName),
                CoinCurrentPrice=VALUES(CoinCurrentPrice), CoinMarketCap=VALUES(CoinMarketCap)
                """
            coin_records = [(coin['id'], coin['symbol'], coin['name'], coin['current_price'], coin['market_cap'])
                            for coin in coins]
            with connection.cursor() as cursor:
                cursor.executemany(query, coin_records)
                connection.commit()
            logger.info('Successfully wrote coins to DB.')
    except Error as err:
        logger.critical(f'MySQL Error: {err}')
    except Exception as err:
        logger.critical(f'Unknown exception: {err}')


def decide_trade():
    """Verify if the current prices of relevant coins are lower than the average price. Place an order if it is,
    otherwise do nothing. Log the results of any trades.

    :rtype: None
    """
    return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO,
                        handlers=[timed_rotate_handler, console_handler])
    logging.info('Crypto sync started.')
    coins = top_three_by_market_cap()
    write_to_db(coins)

    logging.info('Crypto sync ended.')



# try:
#     with connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD) as connection:
#         query = "SHOW DATABASES"
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             for db in cursor:
#                 print(db)
# except Error as e:
#     print(e)

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


def decide_trade(coins, buy_amount=1):
    """Verify if the current prices of relevant coins are lower than the average price. Place an order if it is,
    otherwise do nothing. Log the results of any trades.

    :rtype: None
    """
    for coin in coins:
        price_history = crypto_api.get_coin_price_history(coin['id'])
        price_history_avg = sum([price[1] for price in price_history]) / len(price_history)
        if coin['current_price'] < price_history_avg:
            crypto_api.submit_order(coin['id'], buy_amount, coin['current_price'])
            amount_paid = coin['current_price'] * buy_amount
            logger.info(f"{buy_amount} {coin['name']} purchased for {amount_paid}!")
            try:
                with connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD,
                             database=DB_DATABASE) as connection:
                    with connection.cursor() as cursor:
                        get_pkid_query = f"SELECT ID FROM Coin WHERE CoinID='{coin['id']}' LIMIT 1"
                        cursor.execute(get_pkid_query)
                        coin_pkid = cursor.fetchone()[0]

                        update_portfolio_query = f"""
                        INSERT INTO Portfolio 
                        (CoinID, PortfolioQuantity, PortfolioPaid, PortfolioGain) 
                        VALUES ( {coin_pkid}, {buy_amount}, {amount_paid}, 0 ) 
                        ON DUPLICATE KEY UPDATE CoinID={coin_pkid}, PortfolioQuantity=PortfolioQuantity+{buy_amount}, 
                        PortfolioPaid=PortfolioPaid+{amount_paid}, PortfolioGain=PortfolioGain
                        """
                        cursor.execute(update_portfolio_query)
                        connection.commit()
                    logger.info('Successfully updated purchase to the portfolio.')
            except Error as err:
                logger.critical(f'MySQL Error: {err}')
                logger.critical(f'Possible problem query: {get_pkid_query}')
                logger.critical(f'Possible problem query: {update_portfolio_query}')
            except Exception as err:
                logger.critical(f'Unknown exception: {err}')


# TODO: This could (and should) probably be done in MySQL directly, maybe as a job or stored procedure
def update_portfolio_gain():
    """Update portfolio gains in the DB.

    :rtype: None
    """
    try:
        logger.info('Starting update of portfolio gains')
        with connect(host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD,
                     database=DB_DATABASE) as connection:
            with connection.cursor() as cursor:
                get_portfolio_query = f"SELECT * FROM Portfolio LIMIT 20"
                cursor.execute(get_portfolio_query)
                print('fired1')
                portfolio = cursor.fetchall()

                # coin formatted: (1, 1, 5, Decimal('147889.00') -> (ID, CoinID [FK], Qty, paid)
                for coin in portfolio:
                    get_coin_value_query = f"SELECT CoinCurrentPrice FROM Coin WHERE ID={coin[1]}"
                    cursor.execute(get_coin_value_query)
                    current_price = cursor.fetchone()[0]
                    print('fired2')

                    current_portfolio_value = coin[2] * current_price
                    gain = ((current_portfolio_value - coin[3]) / coin[3]) * 100

                    gain_update_query = f"UPDATE Portfolio SET PortfolioGain = {gain} WHERE ID={coin[0]}"
                    cursor.execute(gain_update_query)
                    connection.commit()
                    print('fired3')

                    logger.info(f'CoinID {coin[0]} - Qty: {coin[2]} Gain: {gain:.2f}')
        logger.info('Ended update of portfolio gains')
    except Error as err:
        logger.critical(f'MySQL Error: {err}')
        logger.critical(f'Possible problem query: {get_portfolio_query}')
        logger.critical(f'Possible problem query: {get_coin_value_query}')
        logger.critical(f'Possible problem query: {gain_update_query}')
    except Exception as err:
        logger.critical(f'Unknown exception: {err}')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO,
                        handlers=[timed_rotate_handler, console_handler])
    logging.info('Crypto sync started.')
    coins = top_three_by_market_cap()
    write_to_db(coins)
    decide_trade(coins)
    update_portfolio_gain()

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

"""
User:
1. Create user (signup function) - DONE
2. Get user (login function) - DONE

Watchlist:
1. Create a watchlist (...) - DONE
2. add a stock to a watchlist ()
    single function: adds stock to stock table and add stock to watchlist_stock table - DONE
3. remove a stock from a watchlist (remove stock from stock table and watchlist_stock table) - DONE
4. get list of a user's watchlists - DONE
5. get a single watchlist (showing all stocks from that watchlist) from list of user's watchlists - DONE
6. Should I create a "remove_watchlist" function? - can come back later

Stock:
1. Search for a stock (API)
2. Get stock's info (API)
"""

from models import db, User, Watchlist, WatchlistStock, Stock


def create_watchlist(name, user_id):
    """Creates a new watchlist."""
    watchlist = Watchlist(
        name = name, 
        user_id = user_id
        )
    
    db.session.add(watchlist)
    db.session.commit()

    return watchlist

def add_stock_to_watchlist(ticker, company_name, stock_url, watchlist_id):
    """Creates a new stock object and adds it to a watchlist."""
    stock_res = Stock.query.filter(Stock.ticker == ticker).all()
    # print(stock_res)

    if len(stock_res) == 0:
        stock = Stock(
            ticker = ticker,
            company_name = company_name,
            stock_url = stock_url
        )

        db.session.add(stock)
        db.session.commit()
    else:
        stock = stock_res[0]

    watchlist_stock = WatchlistStock(
        watchlist_id = watchlist_id,
        stock_id = stock.id
    )

    db.session.add(watchlist_stock)
    db.session.commit()

def remove_stock_from_watchlist(stock_id, watchlist_id):
    """Removes a stock from a watchlist."""
    WatchlistStock.query.filter(WatchlistStock.stock_id == stock_id, WatchlistStock.watchlist_id == watchlist_id).delete()

    db.session.commit()

    """
    DELETE FROM watchlist_stock
    WHERE watchlist_stock.stock_id = stock_id(python)
    AND watchlist_stock.watchlist_id = watchlist_id(python)
    """

    # watchlist_stock = WatchlistStock.query.get(stock_id)
    # watchlist = WatchlistStock.query.get(watchlist_id)

    # db.session.delete(watchlist_stock)
    # db.session.delete(watchlist)
    # db.session.commit()

def get_watchlists(user_id):
    """Gets all of a user's watchlists."""
    # user = User.query.get(user_id)

    watchlists = Watchlist.query.filter(Watchlist.user_id == user_id).all()

    return watchlists

def get_watchlist(watchlist_id):
    """Gets a single watchlist and all the stocks inside that watchlist."""
    result = db.session.query(Stock).join(WatchlistStock, Stock.id == WatchlistStock.stock_id).filter(WatchlistStock.watchlist_id == watchlist_id).all()

    return result
    
    """
    SELECT watchlist_stock.watchlist_id, stocks.ticker, stocks.company_name
    FROM watchlist_stock
    JOIN stocks ON watchlist_stock.stock_id = stocks.id
    WHERE watchlist_stock.watchlist_id = (python variable);

    stock_id  |  stocks.id  | watchlist_id  |  ticker  |  name  |  url
    """

    # print('Avi1')
    # print(result)
    # print(type(result))
    # print(result[0].stock_url)

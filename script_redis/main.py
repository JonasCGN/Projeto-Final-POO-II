from src.bd import DB_Redis

if __name__ == '__main__':
    db = DB_Redis()
    db.test_connection()

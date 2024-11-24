import redis


class DB_Redis:

    def __init__(self):
        self.redis_client = redis.Redis(
            host='redis', port=6379, decode_responses=True)

    def test_connection(self):
        try:
            self.redis_client.ping()
            print("Conexão com o Redis estabelecida com sucesso!")
        except redis.ConnectionError:
            print("Não foi possível conectar ao Redis.")

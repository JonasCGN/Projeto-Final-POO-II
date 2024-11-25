import redis

class DB_Redis:

    def __init__(self):
        self.redis_client = redis.Redis(
            host='redis', port=6379, decode_responses=True)
        self.set_initial_values()
    
    def set_initial_values(self):
        self.qtd_removidos = self.get('qtd_removidos')
        self.qtd_inseridos = self.get('qtd_inseridos')

        if self.qtd_removidos is None:
            self.insert('qtd_removidos', 0)

        if self.qtd_inseridos is None:
            self.insert('qtd_inseridos', 0)

    def test_connection(self):
        try:
            self.redis_client.ping()
            print("Conexão com o Redis estabelecida com sucesso!")
        except redis.ConnectionError:
            print("Não foi possível conectar ao Redis.")

    def insert(self, key, value):
        self.redis_client.set(key, value)

    def increment(self, key):
        self.redis_client.incr(key)

    def decrement(self, key):
        self.redis_client.decr(key)

    def get(self, key):
        return self.redis_client.get(key)

import redis

# Conectar ao Redis no WSL
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Testar a conexão
try:
    redis_client.ping()
    print("Conexão com o Redis estabelecida com sucesso!")
except redis.ConnectionError:
    print("Não foi possível conectar ao Redis.")

# Usar comandos Redis
redis_client.set('chave', 'valor')
valor = redis_client.get('chave')
print(f"O valor armazenado na chave é: {valor}")

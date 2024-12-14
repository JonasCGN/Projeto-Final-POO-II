from src.send_to_redis import SenderToRedis

qtd_requests = 1_000_000

if __name__ == '__main__':
    sender = SenderToRedis()
    sender.run(qtd_requests, 10)

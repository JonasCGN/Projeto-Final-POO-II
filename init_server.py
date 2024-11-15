from src.servidor import Servidor

if __name__ == "__main__":
    servidor = Servidor()
    servidor.init()
    while True:
        servidor.connect_user()
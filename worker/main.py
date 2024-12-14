from libary.sincronizacao import Sincronizacao
from time import sleep

if __name__ == '__main__':
    sincronizacao = Sincronizacao()
    while True:
        sincronizacao.run(10)
        sleep(5)

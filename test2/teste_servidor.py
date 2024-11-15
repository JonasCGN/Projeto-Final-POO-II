from servidor import Servidor

def teste_servidor():
    servidor = Servidor()
    servidor.start()

    print("Servidor iniciado.")

    while True:
        try:
            comando = input("Digite 'exit' para encerrar o servidor: ")
            if comando == 'exit':
                servidor.stop()
                break
        except KeyboardInterrupt:
            servidor.stop()
            break
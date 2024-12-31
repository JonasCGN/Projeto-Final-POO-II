all: databese_up creat_paste_bibs build_bib_funcao_postgree build_bib_sincronizacao_servidor_cliente build_bib_bib_email_functions
server: all install_requeriments run_server
cliente: all install_requeriments run_cliente

install_depedencia:
	@sudo apt-get install python3-venv python3-pip docker.io docker-compose python3-poetry -y

venv:
	@test -d .venv || python3 -m venv .venv
	@chmod -R u+x .venv
	# @source .venv/bin/activate

clear:
	@rm -rf server/bibs
	@rm -rf cliente/bibs
	@rm -rf bib_funcao_postgree/dist
	@rm -rf bib_sincronizacao_servidor_cliente/dist


databese_up:
	@sudo docker-compose up -d --build 

creat_paste_bibs:
	@mkdir cliente_and_server/bibs -p

build_bib_funcao_postgree:
	@cd bib_funcao_postgree && make
	@cp ./bib_funcao_postgree/dist/funcao_postgree-0.1.0-py3-none-any.whl ./cliente_and_server/bibs/

build_bib_sincronizacao_servidor_cliente:
	@cd bib_sincronizacao_servidor_cliente && make
	@cp ./bib_sincronizacao_servidor_cliente/dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl ./cliente_and_server/bibs/

build_bib_bib_email_functions:
	@cd bib_email_functions && make
	@cp bib_email_functions/dist/email_functions-0.1.0-py3-none-any.whl ./cliente_and_server/bibs/

install_requeriments:
	@cd cliente_and_server && pip install bibs/funcao_postgree-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente_and_server && pip install bibs/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente_and_server && pip install bibs/email_functions-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente_and_server && pip install -r requirements.txt

run_server:
	@clear
	@cd cliente_and_server && python3 main_server.py

run_cliente:
	@clear
	@cd cliente_and_server && python3 main_cliente.py
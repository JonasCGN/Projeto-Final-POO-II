all: creat_paste_bibs build_bib_funcao_postgree build_bib_sincronizacao_servidor_cliente
server: all install_requeriments_server run_server
cliente: all install_requeriments_cliente run_cliente

creat_paste_bibs:
	mkdir server/bibs -p
	mkdir cliente/bibs -p

build_bib_funcao_postgree:
	@cd bib_funcao_postgree && make
	cp ./bib_funcao_postgree/dist/funcao_postgree-0.1.0-py3-none-any.whl ./cliente/bibs/
	cp ./bib_funcao_postgree/dist/funcao_postgree-0.1.0-py3-none-any.whl ./server/bibs/

build_bib_sincronizacao_servidor_cliente:
	@cd bib_sincronizacao_servidor_cliente && make
	cp ./bib_sincronizacao_servidor_cliente/dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl ./cliente/bibs/
	cp ./bib_sincronizacao_servidor_cliente/dist/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl ./server/bibs/

install_requeriments_server:
	@cd server && pip install bibs/funcao_postgree-0.1.0-py3-none-any.whl --force-reinstall
	cd server && pip install bibs/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl --force-reinstall
	cd server && pip install -r requirements.txt

install_requeriments_cliente:
	@cd cliente && pip install bibs/funcao_postgree-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente && pip install bibs/sincronizacao_servidor_cliente-0.1.0-py3-none-any.whl --force-reinstall
	@cd cliente && pip install -r requirements.txt

run_server:
	@cd server && python3 main.py

run_cliente:
	@cd cliente && python3 main.py
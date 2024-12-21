all: creat_paste_bibs build_bib_postgre_func install_requeriments_server
server: all run_server
cliente: all run_cliente

creat_paste_bibs:
	@mkdir server/bibs -p
	@mkdir cliente/bibs -p

build_bib_postgre_func:
	@cd bib_postgre_func && make
	@cp ./bib_postgre_func/dist/postgre_func-0.1.0-py3-none-any.whl ./cliente/bibs/
	@cp ./bib_postgre_func/dist/postgre_func-0.1.0-py3-none-any.whl ./server/bibs/

install_requeriments_server:
	@cd server && pip install bibs/postgre_func-0.1.0-py3-none-any.whl --force-reinstall
	@cd server && pip install -r requirements.txt

run_server:
	@cd server && python3 main.py

run_cliente:
	@cd cliente && python3 main.py
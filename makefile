all: creat_paste_bibs build_bib_postgre_func build_bib_product_maneger

creat_paste_bibs:
	@mkdir server/bibs -p
	@mkdir cliente/bibs -p

build_bib_postgre_func:
	@cd bib_postgre_func && make
	@cp ./bib_postgre_func/dist/postgre_func-0.1.0-py3-none-any.whl ./cliente/bibs/
	@cp ./bib_postgre_func/dist/postgre_func-0.1.0-py3-none-any.whl ./server/bibs/

build_bib_product_maneger:
	@cd bib_produt_maneger && make
	@cp ./bib_produt_maneger/dist/produt_maneger-0.1.0-py3-none-any.whl ./cliente/bibs/
	@cp ./bib_produt_maneger/dist/produt_maneger-0.1.0-py3-none-any.whl ./server/bibs/

# docker_run:
# 	@sudo docker-compose up --build -d
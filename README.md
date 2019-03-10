Comparador de imagenes

Instalacion:
* git clone https://github.com/gpiotti/image_comparer.git
* python image_comparer_build.py
* python image_comparer_server.py

Uso:
* request de ejemplo
	http://localhost:5000/?url_1=http://mlu-s1-p.mlstatic.com/878414-MLU28995916846_122018-O.jpg&url_2=http://mlu-s1-p.mlstatic.com/822514-MLU28996049521_122018-O.jpg

* script para comparar imagenes desde MercadoLibre Api
	python batch_compare.py "chromecast" "5" "1"
	1er arg = query
	2do arg = limite de productos para comparar
	3er arg = 1 excluir matches exactos, 0 incluir matches exactos

	Devuelve una lista con el top 10 de matches



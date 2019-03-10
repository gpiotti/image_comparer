import image_comparer
import pytest

my_image_comparer = image_comparer.Image_comparer.load()


def test_response():
	url_1 = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
	url_2 = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
	results = my_image_comparer.compare_images(url_1, url_2)
	assert results[0] == url_1,  "first item should be url_1"
	assert results[1] == url_2,  "second_item_should be url_2"

def test_equal():
	url_1 = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
	url_2 = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
	results = my_image_comparer.compare_images(url_1, url_2)
	assert results[3] == 1,  "equal flag should be 1 if images are equal"
	

def test_not_equal():
	url_1 = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
	url_2 = "https://images-na.ssl-images-amazon.com/images/I/515Znj9pgdL._SL1024_.jpg"
	results = my_image_comparer.compare_images(url_1, url_2)
	assert results[3] == 0,  "equal flag should be 0 if images aren't equal"

def test_similar():
	url_1 = "https://images-na.ssl-images-amazon.com/images/I/41BR18ZkssL.jpg"
	url_2 = "https://http2.mlstatic.com/25535-r20-llanta-hankook-k120-ventus-v12-evo2-97-y-D_NQ_NP_657377-MLM25985510474_092017-O.webp"
	results = my_image_comparer.compare_images(url_1, url_2)
	assert results[3] == 0,  "equal flag should be 0 if images aren't equal"



	


	


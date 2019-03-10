import image_comparer
import requests
import json
from itertools import combinations
import time

query_base = "https://api.mercadolibre.com/sites/MLU/search?q="
item_qry_base = "https://api.mercadolibre.com/items/"


qry_response = requests.get(query_base + "chromecast")
qry_parsed =  json.loads(qry_response.text)



items = [x['id'] for x in qry_parsed['results']]

pictures = []
for item in items:
    qry = item_qry_base + item
    response = requests.get(qry)
    parsed = json.loads(response.text)
    for img in parsed['pictures']:
        pictures.append(img['url'])

comb = list(combinations(pictures, 2))
print( "About to do {0} comparisons".format(len(comb)))

tic = time.time()

my_image_comparer = image_comparer.Image_comparer.load()

matches = []

for i,j  in comb: 

    tmp = my_image_comparer.compare_images(i, j, False)
    if tmp[3] == 0:
        matches.append(tmp)

toc = time.time()


matches = sorted(matches, key = lambda x: int(x[2]), reverse=True)
print(matches[0:50])

print("\nTime taken: {0:.2f} secs".format(toc - tic))



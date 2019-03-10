import image_comparer
import requests
import json
from itertools import combinations
import time
from pprint import pprint
import sys

query_base = "https://api.mercadolibre.com/sites/MLU/search?q="
item_qry_base = "https://api.mercadolibre.com/items/"




try:
    query_item = sys.argv[1]
except IndexError:
    query_item = "chromecast"
    
try:
    items_limit = int(sys.argv[2])
except IndexError:
    items_limit = 2
    
try:
    exclude_exact = int(sys.argv[3])
except IndexError:
    exclude_exact = 1
    
qry_response = requests.get(query_base + query_item)
qry_parsed =  json.loads(qry_response.text)
    
print("Item limit: {0}".format(items_limit)) 
items = [x['id'] for x in qry_parsed['results']]

pictures = []
for item in items[0:items_limit]:
    qry = item_qry_base + item
    response = requests.get(qry)
    parsed = json.loads(response.text)
    for img in parsed['pictures']:
        pictures.append(img['url'])

comb = list(combinations(pictures, 2))
print( "About to do {0} image comparisons".format(len(comb)))

tic = time.time()

my_image_comparer = image_comparer.Image_comparer.load()

matches = []

for ix, val  in enumerate(comb): 
    if ix % 10 == 0:
        print("{0:.2f} % Done".format(ix/len(comb)*100), end='\r', flush=True)
    tmp = my_image_comparer.compare_images(val[0], val[1], False)
    if exclude_exact == 1 and tmp[3] == 0:
        matches.append(tmp)
    elif exclude_exact == 0:
        matches.append(tmp)

toc = time.time()


matches = sorted(matches, key = lambda x: int(x[2]), reverse=True)
print("Best non equal matches")
pprint(matches[0:10])

print( "Done {0} comparisons!".format(len(comb)))
print("\nTime taken: {0:.2f} secs".format(toc - tic))



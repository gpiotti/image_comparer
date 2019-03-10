from flask import Flask, request, jsonify
import image_comparer

app = Flask(__name__)


@app.route('/')
def image_comparer2():
    """ Compare Image 1 vs Image 2 given the query 'q' """
    url_img1 = request.args.get('url_1')
    url_img2 = request.args.get('url_2')

    results = my_image_comparer.compare_images(url_img1, url_img2, False)
    return jsonify({"Results": results})

if __name__ == "__main__":
    my_image_comparer = image_comparer.Image_comparer.load()

    app.run()



import image_comparer
import sys


def build():
    my_image_comparer = image_comparer.Image_comparer()
    my_image_comparer.save()

if __name__ == "__main__":
    sys.exit(build())

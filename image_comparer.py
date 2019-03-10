import json
import pickle
import re
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from skimage.measure import compare_ssim as ssim
import cv2
from sklearn.metrics.pairwise import cosine_similarity

#test_cartel = "https://images-americanas.b2w.io/produtos/01/00/sku/10835/3/10835379_1GG.jpg"
#test_cartel_zoom = "https://http2.mlstatic.com/fivela-medicina-veterinaria-master-9957-unico-D_NQ_NP_348701-MLB20411894381_092015-F.webp"
#test_na = "https://http2.mlstatic.com/resources/frontend/statics/img-not-available/1.1.0/F.gif"
#test_llanta = "https://http2.mlstatic.com/25535-r20-llanta-hankook-k120-ventus-v12-evo2-97-y-D_NQ_NP_657377-MLM25985510474_092017-O.webp"
#test_llanta_crop = "https://images-na.ssl-images-amazon.com/images/I/41BR18ZkssL.jpg"
#test_frasco = "https://http2.mlstatic.com/frasco-ball-mason-jar-8oz-5cm-boca-regular-tarro-vaso-D_NQ_NP_861098-MLM25878179628_082017-F.webp"
#test_zapatos = "https://images-na.ssl-images-amazon.com/images/I/61oTtBphkNL._SL1050_.jpg"
#test_ant_1= "https://http2.mlstatic.com/oakley-jupiter-squared-polished-black-prizm-black-polarized-D_NQ_NP_840899-MLM26116185041_102017-F.webp"
#test_ant_2= "https://images-na.ssl-images-amazon.com/images/I/61SYtu0x1XL._SL1500_.jpg"

DEFAULT_FILENAME = "image_comparer.pkl"


class Image_comparer:
    def __init__(self):
        self.size = 512, 512
        #for good matches scoring
        self.good_match_distance_factor = 0.75 
        #ORB parameters
        self.edgeThreshold = 5
        self.patchSize = 31
        self.nlevels = 7
        self.scaleFactor = 1.2
        self.WTA_K = 2
        self.scoreType = cv2.ORB_FAST_SCORE
        self.firstLevel = 0
        self.nfeatures = 500
            
    def get_from_url(self, url, sanityCheck=True):
        #OpenCV no soport GIF, asi que lo abro con pillow y se lo paso
        
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert('L')
        open_cv_image = np.array(img)
        #open_cv_image = cv2.imdecode(np.asarray(bytearray(img)), 0)
        #open_cv_image = cv2.imdecode(np.asarray(bytearray(response.content)), 0)
        return open_cv_image
    
    def check_equal(self, img1, img2, verbose=False):
        are_equal = False
        img1 = cv2.resize(img1, self.size, interpolation = cv2.INTER_AREA)
        img2 = cv2.resize(img2, self.size, interpolation = cv2.INTER_AREA)
        difference = cv2.subtract(img1, img2)
        
        are_equal = True if np.count_nonzero(difference) == 0 else False
                
        if verbose == True:
            if are_equal == True:
                print("The images are completely Equal")
            else:
                print("The images are NOT equal")
        return are_equal
                
         
    def save(self, filename=DEFAULT_FILENAME):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename=DEFAULT_FILENAME):
        with open(filename, "rb") as f:
            return pickle.load(f)
        
    def get_similarity_score(self, img1, img2, verbose=False):     
       
        orb = cv2.ORB_create(
                edgeThreshold = self.edgeThreshold,
                patchSize = self.patchSize,
                nlevels = self.nlevels,  
                scaleFactor = self.scaleFactor,
                WTA_K = self.WTA_K,
                scoreType = self.scoreType,
                firstLevel = self.firstLevel,
                nfeatures = self.nfeatures)
        
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = bf.match(des1, des2)
        
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        
        good = []
        for m,n in matches:
            if m.distance < self.good_match_distance_factor * n.distance:
                good.append([m])
     

        number_keypoints = 0
        if len(kp1) <= len(kp2):
            number_keypoints = len(kp1)
        else:
            number_keypoints = len(kp2)
        
        match_score = len(good) / number_keypoints * 100
        
        if verbose==True:
            print("Image 1 shape: {0}".format(img1.shape))
            print("Image 2 shape: {0}".format(img2.shape))

            print("Keypoints 1ST Image: {0}".format(len(kp1)))
            print("Keypoints 2ND Image: {0}".format(len(kp2)))
            print("GOOD Matches: {0}".format(len(good)))
            print("How good it's the match: {0}".format(match_score))

            img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    
            plt.imshow(img3)
            plt.show()
            
        return match_score
            
    def compare_images(self, url_img1, url_img2, verbose=False):
        img1 = self.get_from_url(url_img1)
        img2 = self.get_from_url(url_img2)
        
        are_equal = self.check_equal(img1, img2, verbose)
        match_score = self.get_similarity_score(img1, img2, verbose)
        
        return [url_img1, url_img2, match_score, int(are_equal)]

#my_image_comparer = Image_comparer()
##my_image_comparer.compare_images(test_na, test_na)
#my_image_comparer.compare_images(test_frasco, test_frasco)
#my_image_comparer.compare_images(test_llanta, test_llanta_crop)
#my_image_comparer.compare_images(test_cartel, test_cartel_zoom)
#my_image_comparer.compare_images(test_zapatos, test_na)
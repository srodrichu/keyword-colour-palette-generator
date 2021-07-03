import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.image as mpimg
import os
from scipy import ndimage, misc
import imageio
import glob
from pinterestspider import PinterestScraper
import urllib.request
from progress.bar import IncrementalBar


class DominantColours:
    
    CLUSTERS = None
    IMAGE = None
    COLOURS = None
    LABELS = None
    
    def __init__(self,image,clusters = 3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def url_to_image(self):

    # download the image, convert it to a NumPy array, and then read

    # it into OpenCV format

        resp = urllib.request.urlopen(self.IMAGE)

        image = np.asarray(bytearray(resp.read()), dtype="uint8")

        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # return the image

        return image
        
    def dominantColours(self):

        '''
        # read image
        
        image = cv2.imread(self.IMAGE)
        
        # convert to rgb from bgr
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        '''

        image = self.url_to_image()

        # reshaping to a list of pixels
        
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        
        # save image
        
        self.IMAGE = image
        
        # k-means to cluster pixels
        
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(image)
        
        # the cluster centres are out dominant colours
        
        self.COLOURS = kmeans.cluster_centers_
        
        #save labels
        
        self.LABELS = kmeans.labels_
        
        # returning after converting to integer from float
        
        return self.COLOURS.astype(int)
    
    def rgb_to_hex(self,rgb):
        
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def plotClusters(self):
        
        # plotting
        
        fig = plt.figure()
        
        ax = Axes3D(fig)
        
        for label, pix in zip(self.LABELS, self.IMAGE):
            ax.scatter(pix[0], pix[1], pix[2], color = self.rgb_to_hex(self.COLOURS[label]))
            
        plt.show()

    def plotHistogram(self):

        numLabels = np.arange(0, self.CLUSTERS+1)

        (hist, _) = np.histogram(self.LABELS, bins = numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()

        colours = self.COLOURS

        colours = colours[(-hist).argsort()]
        hist = hist[(-hist).argsort()] 

        chart = np.zeros((100,500,3), np.uint8)
        start = 0

        for i in range(self.CLUSTERS):
            end = start + (500 / self.CLUSTERS)
            r = colours[i][0]
            g = colours[i][1]
            b = colours[i][2]


        #using cv2.rectangle to plot colors
            cv2.rectangle(chart, (int(start), 0), (int(end), 100), (r,g,b), -1)
            start = end 
        
        #display chart
        plt.figure()
        plt.axis("off")
        plt.imshow(chart)

        '''

        #convert and read our image
        img = cv2.imread(image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #show our image
        plt.figure()
        plt.axis("off")
        plt.imshow(img)

    '''

    def accaKmeans(self,acca):

        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(acca)
        
        # the cluster centres are out dominant colours
        
        self.COLOURS = kmeans.cluster_centers_
        
        #save labels
        
        self.LABELS = kmeans.labels_
        
        # returning after converting to integer from float
        
        return self.COLOURS.astype(int)

def multiRGB(path):

    acca_rgb = []

    '''

    folder = glob.glob(path + '/*.jpeg') # If you have a folder of images you want to iterate through.

    # iterate through the images in a folder and compile a list of dominant colours. more clusters (10 per images)

    '''
    
    bar = IncrementalBar('Progress', max = len(path))

    for i in path:

        bar.next()

        clusters = 10

        dc = DominantColours(i, clusters)

        colours = dc.dominantColours()

        acca_rgb.append(colours)

    acca_rgb = np.concatenate(acca_rgb)

    return acca_rgb

    
def accaPlot(path, clusters = 5):       

    acca = multiRGB(path)

    dc = DominantColours(acca, clusters)

    acca_colours = dc.accaKmeans(acca)

    dc.plotHistogram()

    plt.show()

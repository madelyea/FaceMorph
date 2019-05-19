import numpy as np
import cv2
import sys
import imageio
from delaunay import CalcDelaunay
from points import FeaturePoints


class Image:
    def __init__(self, image):
        self.img = cv2.imread(image)
        self.__name = image

    def __str__(self):
        return self.__name

def affineTransform(src, srcTri, dstTri, size) :
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri))
                                     
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst

def readPoints(path) :
    points = [];
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))
    return points

def triMorph(img1, img2, img, t1, t2, t, alpha) :

    # Each triangle has a rectangle bounding it
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))

    t1Rect = []
    t2Rect = []
    tRect = []

    for i in xrange(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling the triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])

    #find two warped images using the affine transform
    warpImage1 = affineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = affineTransform(img2Rect, t2Rect, tRect, size)
    
    #blend the two warped images using alpha
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # copy this to the morphed image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask


if __name__ == '__main__' :

    print('==================================================')
    print('PSU CS 410/510, Winter 2019, Final Project')
    print('==================================================')
    
    # ===================================
    # example:
    # python faceMorph.py face0.jpg face1.jpg
    # ===================================
    
   
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

        # Read images
    img1 = cv2.imread(filename1);
    img2 = cv2.imread(filename2);
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    #These create the .txt files for feature points of each image
    x = FeaturePoints(filename1)
    x.get_coors() 

    x = FeaturePoints(filename2)  
    x.get_coors()
       
    # read two lists of feature points
    points1 = readPoints(filename1 + '.txt')
    points2 = readPoints(filename2 + '.txt')
    
    #Loops through to save images at different alpha values
    a = 0
    alpha = 0.1
    while alpha < 1: 
        # Compute the average of the two sets of feature points, using alpha
        points = [];
        for i in xrange(0, len(points1)):
            x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
            y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
            points.append((x,y))

        #calculate the Delaunay triangulation
        dt = CalcDelaunay()

        for s in points:
            dt.addFP(s)

        dt.exportTriangles()   #this creates the tri.txt file

        morphedImage = np.zeros(img1.shape, dtype = img1.dtype)

        # Read triangles from tri.txt and morph them
        with open("tri.txt") as file :
            for line in file :
                x,y,z = line.split()

                x = int(x)
                y = int(y)
                z = int(z)

                t1 = [points1[x], points1[y], points1[z]]
                t2 = [points2[x], points2[y], points2[z]]
                t = [points[x], points[y], points[z]]

                # morph a single triangle
                triMorph(img1, img2, morphedImage, t1, t2, t, alpha)       

        cv2.imwrite('Morphed{0}.jpg'.format(a+1),morphedImage)      #saves a different name every iteration
        alpha += 0.1
        a += 1

#Creates a GIF that morphs forwards and backwards and saves it as faceMorph.gif
with imageio.get_writer('faceMorph.gif', mode='I') as writer:
    image = imageio.imread("Morphed1.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed2.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed3.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed4.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed5.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed6.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed7.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed8.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed9.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed10.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed9.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed8.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed7.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed6.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed5.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed4.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed3.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed2.jpg")
    writer.append_data(image)
    image = imageio.imread("Morphed1.jpg")
    writer.append_data(image)
import dlib
import numpy as np
import cv2


class FeaturePoints: 
    def __init__(self, img):
        self.predictor_path = "shape_predictor_68_face_landmarks.dat"
        
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.predictor_path)
        
        self.name = img
        self.img = cv2.imread(img)
        self.dets = self.detector(self.img)

    def get_coors(self):
        save_coordinates = open(self.name + '.txt', 'w') 
        
        for k, d in enumerate(self.dets):
            shape = self.predictor(self.img, d)
        
        vec = np.empty([68, 2], dtype = int)
        
        for b in range(68): 
            vec[b][0] = shape.part(b).x
            vec[b][1] = shape.part(b).y
            save_coordinates.write(str(vec[b][0]) + " "+ str(vec[b][1]) + "\n") 

        extra_points = ['514 360', '294 676', '0 680', '599 588', '0 0', '0 400', '0 799', '300 799',
             '599 799', '599 400', '599 0' , '300 0']
        
        for i in range(len(extra_points)): 
            save_coordinates.write(extra_points[i] + "\n")
        
        save_coordinates.close() #this closes the picture


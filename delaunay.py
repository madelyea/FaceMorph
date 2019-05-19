import numpy as np
from math import sqrt


class CalcDelaunay:
    
    def __init__(self, center = (0,0), radius=9999):
        
        self.triangles = {}
        self.circles = {}

        center = np.asarray(center)
        #corners
        self.coords = [center+radius*np.array((-1, -1)),
                       center+radius*np.array((+1, -1)),
                       center+radius*np.array((+1, +1)),
                       center+radius*np.array((-1, +1))]

        Tri1 = (0, 1, 3)
        Tri2 = (2, 3, 1)
        self.triangles[Tri1] = [Tri2, None, None]
        self.triangles[Tri2] = [Tri1, None, None]

        # Find circumcenters and circumradius for triangle T1 and T2
        for t in self.triangles:
            self.circles[t] = self.circumcenter(t)
    
    #The circumcenter is the center of the circle formed from the three points of a triangle
    #This function returns the center and radius of a triangle's circumcircle
    def circumcenter(self, tri):
        #https://en.wikipedia.org/wiki/Circumscribed_circle#Circumcircle_equations
        pts = np.asarray([self.coords[v] for v in tri])
        pts2 = np.dot(pts, pts.T)
        A = np.bmat([[2 * pts2, [[1],
                                 [1],
                                 [1]]],
                      [[[1, 1, 1, 0]]]])

        b = np.hstack((np.sum(pts * pts, axis=1), [1]))
 
        x = np.linalg.solve(A, b)
        new_coords = x[:-1]
        c = np.dot(new_coords, pts)
        r = np.sum(np.square(pts[0] - c))
        return (c, r)
    
    #This function checks if a point is in the circumcircle of a triangle
    def checkCircumcircle(self, tri, p):
        c, r = self.circles[tri]   #get the center and radius of triangle that's passed in
        return r >= np.sum(np.square(c - p)) #check to see if the point p lies in the circumcircle 

    #This function adds a feature point to the Delauney Triangulation and adjusts neighboring triangles using the Bowyer-Watson Alg
    #https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    def addFP(self, p):
        p = np.asarray(p)
        idx = len(self.coords)
      
        self.coords.append(p)
        
        badTriangles = []
        # first find all the triangles that are no longer valid due to the insertion
        for T in self.triangles:
            if self.checkCircumcircle(T, p):  #if point is inside circumcircle of triangle add triangle to badTriangles
                badTriangles.append(T)

        polygon = []
        T = badTriangles[0]
        edge = 0
       
        while True:   #// find the boundary of the polygonal hole
            ext_tri = self.triangles[T][edge]
            if ext_tri not in badTriangles:      #if edge is not shared by any other triangles in badTriangles add edge to polygon 
                polygon.append((T[(edge+1) % 3], T[(edge-1) % 3], ext_tri))

                # go to the next edge in the triangle
                edge = (edge + 1) % 3
                
                if polygon[0][0] == polygon[-1][1]:
                    break
            else:
                #go to next edge
                edge = (self.triangles[ext_tri].index(T) + 1) % 3
                T = ext_tri

        # Remove triangles from the data structure
        for T in badTriangles:
            del self.triangles[T]
            del self.circles[T]
            
        newTri = []
        #re-triangulate the polygonal hole
        for (edge0, edge1, ext_tri) in polygon:
            T = (idx, edge0, edge1)    #newTri := form a triangle from edge to point

            self.circles[T] = self.circumcenter(T)

            # Set the external triangle to neighbor of T
            self.triangles[T] = [ext_tri, None, None]

            if ext_tri:
                for i, neighbor in enumerate(self.triangles[ext_tri]):
                    if neighbor:
                        if edge1 in neighbor and edge0 in neighbor:
                            # Use new triangle
                            self.triangles[ext_tri][i] = T

            #  add newTri to triangulation
            newTri.append(T)

        # Connect newTri
        N = len(newTri)
        for i, T in enumerate(newTri):
            self.triangles[T][1] = newTri[(i+1) % N]
            self.triangles[T][2] = newTri[(i-1) % N]

    def exportTriangles(self):
        tri = []
        tri = [(a-4, b-4, c-4)
                for (a, b, c) in self.triangles if a > 3 and b > 3 and c > 3]
        tri = np.array(tri)
        height, _ = tri.shape
        triangles = open('tri.txt', "w")
        
        for i in range(height):
            x = tri[i][0]
            y = tri[i][1]
            z = tri[i][2]
                         
            triangles.write(str(x) + " " + str(y) + " " + str(z) + "\n")
                         
        triangles.close()


        



import sys, math

import phone_gyro as pg
import imu
import Quaternions as qt


class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        #""" Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        #""" Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        #""" Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def quaternionRotation(self):
        quaternionR = getUpdatedQuaternion()
        #print('translated : ', quaternionR)
        quaternionR=qt.Quaternion(quaternionR[0],quaternionR[1],quaternionR[2],quaternionR[3])
        vector= qt.Vector(self.x,self.y,self.z)
        new_vector=qt.apply_rotation_on_vector(quaternionR,vector)
        x=new_vector.vx
        y=new_vector.vy
        z=new_vector.vz
        return Point3D(x,z,y)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)






class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        
        self.vertices = [
            Point3D(0, 0, 0),
            Point3D(1, 0, 0),
            Point3D(0, 1, 0),
            Point3D(0, 0, 1),

            Point3D(2, 2, 0),
            Point3D(-2, 2, 0),
            Point3D(-2, -2, 0),
            Point3D(2, -2, 0)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0, 1, (255, 0, 0)),
                      (0, 2, (0, 0, 255)),
                      (0, 3, (0, 255, 0)),

                      (4, 5, (255, 0, 0)),
                      (5, 6, (0, 0, 0)),
                      (6, 7, (0, 0, 0)),
                      (7, 4, (0, 0, 0))]
        self.angle = 0

    def draw(self,vector=None):
        """ Main Loop """
        if vector!=None:
            self.vertices[4]=(Point3D(vector[0][0],vector[0][1],vector[0][2]))
            #print(self.vertices)
            self.faces[3]=((vector[1],vector[2],vector[3]))
            #print(self.faces)

        # It will hold transformed vertices.
        t = []
        square_coord=[]
        for i,v in enumerate(self.vertices):
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            # r = v.rotateX(self.angle).rotateY(self.angle).rotateZ(self.angle)
            if i>3:
                r=v.quaternionRotation()
                square_coord.append(r.y)
                if i == 7:
                    square_coord.append(r.x)
            else :
                r=v
            # Transform the point from 3D to 2D
            p = r.project(  640,  480, 256, 4)
            # p = r.orthoProject()
            # Put the point in the list of transformed vertices
            t.append(p)
        return square_coord
        
def get_throtal_boost(data):
    print('data: ',data)
    acceleration=(data[4]+3)*12
    print('acceleration  :',acceleration)
    del data[4]
    intensity=40
    bias=1160
    out_data=[]
    for i in data:
    #    print('befor speed_vol :',i)
        speed_vol=(i*intensity)
     #   print('after intensity :',speed_vol)
        speed_vol=speed_vol+acceleration
      #  print('after speed_vol :',speed_vol)
        if acceleration<15:
            new_val=0
        elif i>0:
            print()
            new_val=(speed_vol+bias)
        else:
            new_val=-math.sqrt(speed_vol*speed_vol)+bias
        out_data.append(new_val)
    data= [((i*intensity)+bias) if i>0 else -math.sqrt((i*intensity)*(i*intensity))+bias for i in data]
    #print('current  : ',out_data)
    #print('previous  : ',data)
    
    
    return out_data
def getUpdatedQuaternion():
    gyro = [None] * 3
    acc = [None] * 3
    mag= [None] * 3

    readings = pg.getAcc()
    gyro[0] = float(readings[6])
    gyro[1] = float(readings[7])
    gyro[2] = float(readings[8])
    acc[0] = float(readings[2])
    acc[1] = float(readings[3])
    acc[2] = float(readings[4])

    #print('Gyro : ', gyro)
    #print('Acc : ', acc)
    translated = imu.filterUpdate(gyro[0], gyro[1], gyro[2], acc[0], acc[1], acc[2])
    return translated

if __name__ == "__main__":

    sim =Simulation()

    while True:

        # print(readings)
        #((10*translated[1],10* translated[2], 10*translated[3]), 1, 4, (50, 50, 50))
        sum=[0 for i in range(4) ]
        for i in range(10):
            print('calculating avg')
            each=sim.draw()
            sum[0]=sum[0]+each[0]
            sum[1]=sum[1]+each[1]
            sum[2]=sum[2]+each[2]
            sum[3]=sum[3]+each[3]
        average=[each/10 for each in sum]
        print('Average : ',average)
        square_coord=get_throtal_boost(average)
        
        
        
        # sim.draw(((0.5,0.5,0.5),1, 4, (50, 50, 50)))
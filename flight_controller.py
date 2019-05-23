from draw_3d_vector import Simulation, get_throtal_boost
from engine import Motor
import sys

class MotorManager :
    def __init__(self,validate,calibrate):
        self.fr=Motor(4,1500,calibrate)
        self.fl=Motor(23,1500,calibrate)
        self.bl=Motor(26,1500,calibrate)
        self.br=Motor(16,1500,calibrate)
        self.validate=validate
        
    def updateSpeed(self,input_speed):
        if self.validate :
            if input_speed[0]<1500: 
                print('Speed : ',input_speed[0])
                self.fr.runspeed(input_speed[0])
            if input_speed[1]<1500:
                print('Speed : ',input_speed[1])
                self.fl.runspeed(input_speed[1])
            if input_speed[2]<1500: 
                print('Speed : ',input_speed[2])
                self.bl.runspeed(input_speed[2])
            if input_speed[3]<1500:
                print('Speed : ',input_speed[3])
                self.br.runspeed(input_speed[3])





if __name__=="__main__":
    print('start the tihngs')
    
    if len(sys.argv)>1:
        calibrate=bool(sys.argv[1])
        print('calibrate: ',calibrate)
    mm=MotorManager(True,calibrate)
    sim =Simulation()

    while True:

        # print(readings)
        #((10*translated[1],10* translated[2], 10*translated[3]), 1, 4, (50, 50, 50))
        
        sum=[0 for i in range(5) ]
        for i in range(10):
            print('calculating avg')
            each=sim.draw()
            sum[0]=sum[0]+each[0]
            sum[1]=sum[1]+each[1]
            sum[2]=sum[2]+each[2]
            sum[3]=sum[3]+each[3]
            sum[4]=sum[4]+each[4]
        average=[each/10 for each in sum]
        print('Average : ',average)
        
        mm.updateSpeed(average)
        
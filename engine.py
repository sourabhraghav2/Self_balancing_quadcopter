
import os 
import time 
os.system ("sudo pigpiod")
time.sleep(1) 
import pigpio 


class Motor :
    def __init__(self,pin,max_speed,calibrate):
        self.pi = pigpio.pi()
        time.sleep(1)
        self.pin=pin
        self.min_speed=1100
        self.threshold=1300
        self.max_speed=self.verify_speed(max_speed)
        
        print('GPIO  pin: ',self.pin)
        print('Min Speed: ',self.min_speed)
        print('Threshold: ',self.threshold)
        print('Max Speed: ',self.max_speed)
        
        if calibrate: 
            print('calibrating : ',calibrate)
            self.arm()
        
    def verify_speed(self,speed):
        if speed<self.threshold: 
            new_speed=speed
        else :
            new_speed=self.threshold
        
        if speed<self.min_speed:
            new_speed=self.min_speed
        else :
            new_speed=speed
        return new_speed
        
    def arm(self):
        pin=self.pin
        pi=self.pi
        pi.set_servo_pulsewidth(pin, 0)
        time.sleep(2)
        pi.set_servo_pulsewidth(pin, self.max_speed)
        time.sleep(2)
        pi.set_servo_pulsewidth(pin, self.min_speed)
        time.sleep(3)
        print('running')
        
    def runspeed(self,speed):
        pi=self.pi
        speed=self.verify_speed(speed)
        #print('Speed: ',speed)
        pi.set_servo_pulsewidth(self.pin, speed)
        #time.sleep(2)
        #pi.set_servo_pulsewidth(self.pin, 0)
        
if __name__=='__main__':
    motor=Motor(4,1500,True)
    motor.runspeed(1200)
    motor=Motor(23,1500,True)
    motor.runspeed(1100)
    print('end')




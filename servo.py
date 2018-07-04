''' A simple servo class based on the pigpio library
    http://abyz.me.uk/rpi/pigpio/pigs.html#S/SERVO
'''

import time
from subprocess import check_call

# *** GPIO BCM pin numbering is used ***

# Class for the ordinary servo motor
class Servo:
    def __init__(self, pin):
        self.pin = pin

    def forward(self, speed):
        #proc = check_call(["pigs", "s", "6", str(speed)])
        if speed >=0 and speed <= 600:
            speed += 1500
            proc = check_call(["pigs", "s", str(self.pin), str(speed)])
        else:
            print ("Valid servo values: [0 - 600] microseconds")
            self.stop()
#            exit()

    def backward(self, speed):
        if speed >=0 and speed <= 600:
            speed = 1500 - speed
            proc = check_call(["pigs", "s", str(self.pin), str(speed)])
        else:
            print ("Valid servo values: [0 - 600] microseconds")
            self.stop()
#            exit()

    def stop(self):
        #proc = check_call(["pigs", "s", "6", "0"])
        proc = check_call(["pigs", "s", str(self.pin), "0"])

# Class for the opposite servo motor, positioned UpSide-Down on the robot chassis
class UDServo:
    def __init__(self, pin):
        self.pin = pin

    def forward(self, speed):
        if speed >=0 and speed <= 600:
            speed = 1500 - speed
            proc = check_call(["pigs", "s", str(self.pin), str(speed)])
        else:
            print ("Valid servo values: [0 - 600] microseconds")
            self.stop()
#            exit()

    def backward(self, speed):
        if speed >=0 and speed <= 600:
            speed += 1500
            proc = check_call(["pigs", "s", str(self.pin), str(speed)])
        else:
            print ("Valid servo values: [0 - 600] microseconds")
            self.stop()
#            exit()

    def stop(self):
        proc = check_call(["pigs", "s", str(self.pin), "0"])

if __name__ == '__main__':
    M1=Servo(6)
    M2=UDServo(19)
    M1.forward(speed=200)
    M2.forward(speed=200)
    time.sleep(2)
    M1.stop()
    M2.stop()
    time.sleep(1)
    M1.backward(200)
    M2.backward(200)
    time.sleep(2)
    M1.stop()
    M2.stop()

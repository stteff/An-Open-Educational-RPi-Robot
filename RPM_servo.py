# Regulates servo speed to a specified RPM using Propotional Control
# program part counting RPMs is based from site: ModMyPi

import RPi.GPIO as GPIO
import time
from subprocess import check_call
from servo import Servo, UDServo

# The Normal servo
M2 = Servo(6) 
# GPIO pin of photointerrupter sensor
sensor_2 = 14

# The UpSide Down servo
M1 = UDServo(19) 
# GPIO pin of photointerrupter sensor
sensor_1 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_1,GPIO.IN)
GPIO.setup(sensor_2,GPIO.IN)

# Number of Encoder's Disk Positions
encoder_pos = 20
#encoder_pos = 10

# The initial speed (pulse width in microseconds)
# M1 and M2 at 1680 and 1650 respectively
#speed_1 = 1650
#speed_2 = 1650

speed_1 = 150
speed_2 = 150

# Desired RPM
SP_rpm = 70
count_1 = 0
count_2 = 0

# start and end timers
start_1 = 0
start_2 = 0
end_1 = 0
end_2 = 0

def set_start_1():
 	global start_1
 	start_1 = time.time()

def set_start_2():
 	global start_2
 	start_2 = time.time()

# ---------------------------

def set_end_1():
 	global end_1
 	end_1 = time.time()

def set_end_2():
 	global end_2
 	end_2 = time.time()

# ---------------------------

def inc_speed_1(d):
    global speed_1
    speed_1 += d
    M1.forward(speed_1)
    print ("speed_1: ",speed_1)

def inc_speed_2(d):
    global speed_2
    speed_2 += d
    M2.forward(speed_2)
    print ("speed_2: ",speed_2)

# ---------------------------

def dec_speed_1(d):
    global speed_1
    speed_1 -= d
    M1.forward(speed_1)
    print ("speed_1: ",speed_1)

def dec_speed_2(d):
    global speed_2
    speed_2 -= d
    M2.forward(speed_2)
    print ("speed_2: ",speed_2)

# ---------------------------

def calc_rpm_1():
    global rpm_1
    # The end time
    set_end_1()
    # The net time taken to complete [encoder_pos=20] positions i.e. 1 full
    # rotation in seconds
    dt_1 = end_1 - start_1
    #dt_1 = 2*(end_1 - start_1)
    # 1 Revolution Per Minute ***
    rpm_1 = 60 / dt_1
    print ("RPM_1: ",rpm_1)

def calc_rpm_2():
    global rpm_2
    # The end time
    set_end_2()
    # The net time taken to complete [encoder_pos=20] positions i.e. 1 full
    # rotation in seconds
    dt_2 = end_2 - start_2
    #dt_2 = 2*(end_2 - start_2)
    # 1 Revolution Per Minute ***
    rpm_2 = 60 / dt_2
    print ("RPM_2: ",rpm_2)
# ---------------------------

def get_rpm_1(c):
    global count_1
    global speed_1

#    if not count_1:
        # When count==0, start the timer
#        set_start_1()
#        count_1 += 1
#    else:
#        count_1 += 1

    if count_1 == 0:
        # When count==0, start the timer
        set_start_1()
    count_1 += 1

    if count_1==encoder_pos:

        calc_rpm_1()

        # This is the Propotional Control
        err_1 = rpm_1 - SP_rpm 
        if err_1 > 0:

            if err_1 >= 20:
                dec_speed_1(10)
            if err_1 < 20 and err_1 >= 10:
                dec_speed_1(5)
            if err_1 < 10 and err_1 >= 5:
                dec_speed_1(2)
            if err_1 < 5 and err_1 >= 2:
                dec_speed_1(1)
           # if err_1 < 1:
           #     print ("speed_1: ",speed_1)

            #print ("speed_1: ",speed_1)

        if err_1 < 0:
            #print("err_1: ", err_1)
            err_1 = abs(err_1)
            if err_1 >= 20:
                inc_speed_1(10)
            if err_1 < 20 and err_1 >= 10:
                inc_speed_1(5)
            if err_1 < 10 and err_1 >= 5:
                inc_speed_1(2)
            if err_1 < 5 and err_1 >= 2:
                inc_speed_1(1)
            #if err_1 < 1:
            #    print ("speed_1: ",speed_1)
            
            #print ("speed_1: ",speed_1)


        calc_rpm_1()

        print
        # Reset count
        count_1 = 0

# ---------------------------

def get_rpm_2(c):
    global count_2
    global speed_2

    if count_2 == 0:
        # When count==0, start the timer
        set_start_2()
    count_2 += 1

    if count_2==encoder_pos:

        calc_rpm_2()

        # This is the Propotional Control
        err_2 = rpm_2 - SP_rpm 
        if err_2 > 0:

            if err_2 >= 20:
                dec_speed_2(10)
            if err_2 < 20 and err_2 >= 10:
                dec_speed_2(5)
            if err_2 < 10 and err_2 >= 5:
                dec_speed_2(2)
            if err_2 < 5 and err_2 >= 2:
                dec_speed_2(1)
            #if err_2 < 1:
            #    print ("speed_2: ",speed_2)

            #print ("speed_2: ",speed_2)

        if err_2 < 0:
            #print("err_2: ", err_2)
            err_2 = abs(err_2)
            if err_2 >= 20:
                inc_speed_2(10)
            if err_2 < 20 and err_2 >= 10:
                inc_speed_2(5)
            if err_2 < 10 and err_2 >= 5:
                inc_speed_2(2)
            if err_2 < 5 and err_2 >= 2:
                inc_speed_2(1)
            #if err_2 < 1:
            #    print ("speed_2: ",speed_2)

            #print ("speed_2: ",speed_2)
            
        calc_rpm_2()

        print
        # Reset count
        count_2 = 0

# ---------------------------

#proc1 = check_call(["pigs", "s", "6", str(speed)])
M1.forward(speed_1)
#M1.backward(speed_1)
GPIO.add_event_detect(sensor_1, GPIO.RISING, callback=get_rpm_1)

M2.forward(speed_2)
#M2.backward(speed_2)
GPIO.add_event_detect(sensor_2, GPIO.RISING, callback=get_rpm_2)

try:
 	while True: # create an infinte loop to keep the script running
 	 	time.sleep(0.1)
except KeyboardInterrupt:
    print "  Quit"
    GPIO.cleanup()
    M1.stop()
    M2.stop()
    exit()


# -*- coding: utf-8 -*-
# Ultrasonic Connections
# gpio 17 --> output (trigger)
# gpio 18 <-- input (echo)

from espeak import espeak
import RPi.GPIO as GPIO
import time
import scratch
from w1thermsensor import W1ThermSensor
from servo import Servo, UDServo

def get_distance(trigger,echo):
    # Send 10us pulse to trigger
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    edge_detect = GPIO.wait_for_edge(echo, GPIO.RISING, timeout = 100) 
    if edge_detect is not None:
        start = time.time()
    else: return 100

    edge_detect = GPIO.wait_for_edge(echo, GPIO.FALLING, timeout = 100) 

    if edge_detect is not None:
        stop = time.time()
    else: return 100

    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34326
    # That was the distance there and back so halve the value
    distance = distance / 2
    return (distance)

def Motors_Stop():
    M1.stop()
    M2.stop()
    stop_time = time.time()
    print("Stop Time ", stop_time)
    tt = stop_time - start_time
    return tt

def get_num_of_pos_1(c):
    global num_of_pos_1
    global start_time
    global flag
    if num_of_pos_1 == 0 and flag == 0:
        start_time = time.time()
        flag = 1
    print("---->  ", start_time)
    num_of_pos_1 += 1
    # Keep sending m1 and m2 positions in Real Time back to Scratch
    s.sensorupdate({'m1_positions' : num_of_pos_1})
    s.sensorupdate({'m2_positions' : num_of_pos_2})
    print("m1: ", num_of_pos_1)

def get_num_of_pos_2(c):
    global num_of_pos_2
    num_of_pos_2 += 1
    print("m2: ", num_of_pos_2)

def listen():
    while True:
        try:
            yield s.receive()
        except scratch.ScratchError:
            raise StopIteration
        except KeyboardInterrupt:
            M1.stop()
            M2.stop()
            # Stop Ultrasonic trigger
            GPIO.cleanup()
            exit()

# Robot Voice Settings
espeak.set_voice("el")
espeak.set_parameter(espeak.Parameter.Pitch, 30)
espeak.set_parameter(espeak.Parameter.Rate, 80)
espeak.set_parameter(espeak.Parameter.Range, 50)

# Temperature sensor Setting
# By default connnects to gpio4
therm_sensor = W1ThermSensor()

GPIO.setmode(GPIO.BCM)

# Ultrasonic sensor Settings
trigger = 17
echo = 18
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
# Set trigger to False (Low)
GPIO.output(trigger, False)

# Photo interrupter Settings
IR1_Detect = 15
IR2_Detect = 14

GPIO.setup(IR1_Detect,GPIO.IN)
GPIO.setup(IR2_Detect,GPIO.IN)

GPIO.add_event_detect(IR1_Detect, GPIO.RISING,
        callback=get_num_of_pos_1)
GPIO.add_event_detect(IR2_Detect, GPIO.RISING,
        callback=get_num_of_pos_2)

# The Servos
# Right motor
M1 = UDServo(19)

# Left motor
M2 = Servo(6)
#----------------------------------
num_of_pos_1 = 0
num_of_pos_2 = 0
Motor_1_on = 0 
Motor_2_on = 0 
positions = 0
m1 = 0
m2 = 0
start_time = 0
flag = 0
dt = []
pp = []

# IP of the Remote Computer Running SCRATCH
#s = scratch.Scratch(host='192.168.1.21',port=42001)
s = scratch.Scratch(host='192.168.2.2',port=42001)
#s = scratch.Scratch(host='10.67.166.171',port=42001)
#s = scratch.Scratch(host='192.168.11.192',port=42001)

print ("We are ready now ...")
#while True:
for msg in listen():
  if msg[0] == 'broadcast':
        # Handle broadcast messages received from Scratch

        # Move Forward 
        if msg[1][0:2] == 'GO':
            if msg[1][2:9] == 'FORWARD':
                pwr = float(msg[1][14:])
                M1.forward(speed = int((pwr+0.0)*5))
                M2.forward(speed = int((pwr+0.1)*5))
        # Move Backward
            elif msg[1][2:10] == 'BACKWARD':
                pwr = float(msg[1][15:])
                M1.backward(speed = int(pwr*5))
                M2.backward(speed = int(pwr*5))
        # Turn Right
            elif msg[1][2:7] == 'RIGHT':
                pwr = float(msg[1][12:])
                M1.backward(speed = int(pwr*5))
                M2.forward(speed = int(pwr*5))
        # Turn Left
            elif msg[1][2:6] == 'LEFT':
                pwr = float(msg[1][11:])
                M1.forward(speed = int(pwr*5))
                M2.backward(speed = int(pwr*5))
        if msg[1][0:4] == 'STOP':
            Motors_Stop()
            s.connect()
            s.sensorupdate({'Motors_stopped' : 1})
            s.sensorupdate({'m1_positions' : num_of_pos_1})
            s.sensorupdate({'m2_positions' : num_of_pos_2})
            num_of_pos_1 = 0
            num_of_pos_2 = 0

        # Speak the text or variable content
        if msg[1][0:5] == 'speak':
            espeak.synth(msg[1][5:])

        # Get Temperature and send it to Scratch
        if msg[1][0:4] == 'temp':
            s.connect()
            s.sensorupdate({'tmp' : therm_sensor.get_temperature()})

        if msg[1][0:4] == 'dist':
            s.connect()
            #pp.append(get_distance(trigger,echo))
            #ds = pp.pop()
            ds = get_distance(trigger,echo)
            s.sensorupdate({'dst' : ds})

        # Hold the last broadcast received
        last_msg = msg[1]
        if msg[1][0:2] == 'm1':
            last_msg = 'm1'
            m1 = float(msg[1][2:])
            if abs(m1) > 0:
                Motor_1_on = 1
            else:
                Motor_1_on = 0
                M1.stop()

        if msg[1][0:2] == 'm2':
            last_msg = 'm2'
            m2 = float(msg[1][2:])
            if abs(m2) > 0:
                Motor_2_on = 1
            else:
                Motor_2_on = 0
                M2.stop()

        if msg[1][0:5] == 'posts':
            last_msg = 'posts'
            positions = int(round(float(msg[1][5:])))
            Motor_1_on = 1
            Motor_2_on = 1
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
        # No other broadcasts accepted exept: m1, m2, posts
        while (Motor_1_on and Motor_2_on) and last_msg in ['m1', 'm2', 'posts']:

            if msg[1][0:2] == 'm1':
                last_msg = 'm1'
                m1 = float(msg[1][2:])
                Motor_1_on = 0

            if (m1 > 0):
                M1.forward(speed = int(m1*5))
            elif (m1 < 0):
                M1.backward(speed = abs(int(m1*5)))

            if msg[1][0:2] == 'm2':
                last_msg = 'm2'
                m2 = float(msg[1][2:])
                Motor_2_on = 0
            
            if (m2 > 0):
                M2.forward(speed = int(m2*5))
            elif (m2 < 0):
                M2.backward(speed = abs(int(m2*5)))

            #  ----------------------------

            if msg[1][0:5] == 'posts':
                last_msg = 'posts'
                positions = int(round(float(msg[1][5:])))
                if positions == 0:
                    Motor_1_on = 0
                    Motor_2_on = 0
                    m1 = 0
                    m2 = 0
                #print ("positions **** ", positions, num_of_pos)

            #print ("AVERAGE POSITIONS: ", (num_of_pos_1+num_of_pos_2)/2)

            if num_of_pos_2 >= positions:
                dt.append(Motors_Stop())
                print("DT 2: ", dt[0])
                s.sensorupdate({'t_motors_on' : dt[0]})
                print(float(num_of_pos_2)/20, " Rotations for m2")
                num_of_pos_2 = 0
                num_of_pos_1 = 0
                # Reset flag to get new start_time at next robot movement
                flag = 0
                break

            if num_of_pos_1 >= positions:
                dt.append(Motors_Stop())
                print("DT 1: ", dt[0])
                s.sensorupdate({'t_motors_on' : dt[0]})
                print(float(num_of_pos_1)/20, " Rotations for m1")
                num_of_pos_2 = 0
                num_of_pos_1 = 0
                flag = 0
                break

            dt = []

  pp = []

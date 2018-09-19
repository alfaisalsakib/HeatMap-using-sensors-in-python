import HMC5883L
import MPU9250
import GY521
import DHT22

import Calibration
import Parameters
import Tools
import State

import _thread
import socket
import time

# Initialize and Calibrate all sensors
sentinel = True
while sentinel:
    try:
        MPU9250.MPU9250_Initialize()
        Calibration.Calibrate_Accelerometer_2_Data()
        print("")

        GY521.MPU6050_Initialize()
        Calibration.Calibrate_Accelerometer_Data()
        Calibration.Calibrate_Raw_Gyroscope_Data()
        print("")

        HMC5883L.HMC5883L_Initialize()
        Calibration.Update_Reference_Orientation()
        print("")
        
        sentinel = False
    except:
        print(" Error!\n")
        time.sleep(2)

_thread.start_new_thread(Tools.Orientation_Thread_Function,())
_thread.start_new_thread(Tools.DHT22_Thread_Function,())

print("Initializing data logging capabilities. . .", end="")
dataLog = open("DataLog.txt","w")
print(" Success!")

print("Attempting connection to client. . .", end="")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
s.bind(('192.168.0.4',10009)) # The server address and port
s.listen(1)
conn,addr=s.accept()

print(" Success!")

print("\nCollecting data. . .")
count = 0
while True:
    try:
        if (State.ERROR_FLAG_1 or State.ERROR_FLAG_2 or State.ERROR_FLAG_3):
            print("\n")
            MPU9250.MPU9250_Initialize()
            GY521.MPU6050_Initialize()
            HMC5883L.HMC5883L_Initialize()
            State.ERROR_FLAG_1 = False
            State.ERROR_FLAG_2 = False
            State.ERROR_FLAG_3 = False
            print("\nResuming data collection. . .")
        
        Tools.Update_Footstep_Count()
        count += 1
        if count == 40:
            count = 0
            dataString = str(abs(round(State.X_POSITION*10,2)))+","+str(abs(round(State.Y_POSITION*10,2)))+","+str(State.HUMIDITY)+","+str(State.TEMPERATURE)
            try:
                print("", end="")
                conn.send(str(int(abs(round(State.X_POSITION*10,2)))).encode()+str(",").encode()+str(int(abs(round(State.Y_POSITION*10,2)))).encode()+str(",").encode()+str(State.HUMIDITY).encode()+str(",").encode()+str(State.TEMPERATURE).encode()+str('\n').encode())
            except:
                break
            
            dataString = dataString+"\n"
            dataLog.write(dataString)
            print("X: %5.2f, Y: %5.2f, H: %5.2f, T: %5.2f @ ORIENTATION: %7.2f -> %3.0f" %(State.X_POSITION, State.Y_POSITION, State.HUMIDITY, State.TEMPERATURE, State.ORIENTATION_MAGNETOMETER_Z, State.DISCRETE_ORIENTATION_Z))
    except:
        print(" Error!")
        State.ERROR_FLAG_1 = True
        time.sleep(2)
        continue
    
    time.sleep(Parameters.GLOBAL_TIME_PERIOD)

try:
    dataLog.close()
    conn.close()
except:
    print("", end="")

print("\nProgram Executed Successfully and Terminated Systematically!")

import Calibration
import Parameters
import HMC5883L
import MPU9250
import GY521
import DHT22
import State

import math
import time

def Orientation_Thread_Function():
    while True:
        try:
            Update_Discrete_Orientation()
            time.sleep(0.01)
        except:
            State.ERROR_FLAG_2 = True
    
    return

def DHT22_Thread_Function():
    while True:
        try:
            DHT22.Probe_Humidity_Temperature()
            time.sleep(2)
        except:
            State.ERROR_FLAG_3 = True
    
    return

def Update_Discrete_Orientation():
    Update_Magnetometer_Orientation()
    reference_absolute_orientation = 180 + State.REFERENCE_ORIENTATION_Z
    current_absolute_orientation = 180 + State.ORIENTATION_MAGNETOMETER_Z
    relative_orientation = current_absolute_orientation - reference_absolute_orientation
    if relative_orientation<0: relative_orientation += 360
    if (relative_orientation>=315) or (relative_orientation<=45): State.DISCRETE_ORIENTATION_Z = 0
    elif (relative_orientation>=45) and (relative_orientation<=135): State.DISCRETE_ORIENTATION_Z = 270
    elif (relative_orientation>=135) and (relative_orientation<=225): State.DISCRETE_ORIENTATION_Z = 180
    elif (relative_orientation>=225) and (relative_orientation<=315): State.DISCRETE_ORIENTATION_Z = 90
    
    return

def Update_Footstep_Count():
    if State.GRAVITIONAL_ACCELERATION_2==0:
        Calibration.Calibrate_Accelerometer_2_Data()
        State.TIME_STAMP = time.perf_counter()
    
    Ax, Ay, Az = MPU9250.Probe_Accelerometer()
    acceleration_magnitude = math.sqrt(Ax*Ax + Ay*Ay + Az*Az) - State.GRAVITIONAL_ACCELERATION_2
    if acceleration_magnitude>Parameters.FOOTSTEP_ACCELERATION_THRESHOLD:
        if State.TIME_STAMP+Parameters.FOOTSTEP_TIME_LOCALITY_THRESHOLD<time.perf_counter():
            State.TIME_STAMP = time.perf_counter()
            State.X_POSITION += Parameters.FOOTSTEP_LENGTH * math.sin(math.radians(State.DISCRETE_ORIENTATION_Z))
            State.Y_POSITION += Parameters.FOOTSTEP_LENGTH * math.cos(math.radians(State.DISCRETE_ORIENTATION_Z))
            # State.FOOTSTEP_COUNT+=1
    
    return

def Update_Velocity_Magnitude():
    State.VELOCITY_MAGNITUDE += Parameters.GLOBAL_TIME_PERIOD * State.ACCELERATION_MAGNITUDE
    return

def Update_Acceleration_Magnitude():
    if State.GRAVITIONAL_ACCELERATION==0:
        Calibration.Calibrate_Accelerometer_Data()
    
    Ax, Ay, Az = GY521.Probe_Accelerometer()
    
    State.ACCELERATION_MAGNITUDE = math.sqrt(Ax*Ax + Ay*Ay + Az*Az) - State.GRAVITIONAL_ACCELERATION
    return

def Update_Accelerometer_Orientation():
    Ax, Ay, Az = GY521.Read_Raw_Accelerometer_Data() # Fetch the instantaneous raw accelerometer data. The raw values are required to perform acceleration vectoring
    
    AzAx = math.sqrt(Ax*Ax + Az*Az) # Calculate the distance between the z and x components of the acceleration vector
    AzAy = math.sqrt(Ay*Ay + Az*Az) # Calculate the distance between the z and y components of the acceleration vector
    # Ensure the angle varies between -180 to +180 degrees
    if Az>0:
        AzAx*=-1
        AzAy*=-1
    
    # Calculate x-axis and y-axis orientation from the accelerometer data and update the program state
    State.ORIENTATION_ACCELEROMETER_X = math.degrees(math.atan2(Ax, AzAy))
    State.ORIENTATION_ACCELEROMETER_Y = math.degrees(math.atan2(Ay, AzAx))
    
    return

def Update_Magnetometer_Orientation():
    Ax, Ay, Az = GY521.Read_Raw_Accelerometer_Data() # Fetch the instantaneous raw accelerometer data. The raw values are required to perform acceleration vectoring
    Mx, My, Mz = HMC5883L.Read_Raw_Magnetometer_Data() # Fetch the instantaneous raw magnetometer data
    
    # Compensate for the hard iron bias on the magnetometer axes readouts
    Mx += Parameters.BIAS_RAW_MAGNETOMETER_X
    My += Parameters.BIAS_RAW_MAGNETOMETER_Y
    Mz += Parameters.BIAS_RAW_MAGNETOMETER_Z
    
    # Compensate for tilt
    roll = math.atan2(Ay, Az)
    
    Az2 = Ay*math.sin(roll) + Az*math.cos(roll)
    pitch = math.atan(-Ax/Az2)
    
    Mz2 = My*math.sin(roll) + Mz*math.cos(roll)
    My2 = Mz*math.sin(roll) - My*math.cos(roll)
    Mx2 = Mx*math.cos(pitch) + Mz2*math.sin(pitch)
    yaw = math.atan2(My2, Mx2)
    
    State.ORIENTATION_MAGNETOMETER_Z = math.degrees(yaw) + Parameters.MAGNETOMETER_ORIENTATION_OFFSET
    return

def Read_Delta_Gyroscope_Orientation():
    Gx, Gy, Gz = GY521.Probe_Gyroscope() # Fetch the instantaneous set of values from the gyroscope. The processed values are useful because they have already compensated for axes bias
    
    # Update the delta orientation values for the gyroscope
    # State.DELTA_ORIENTATION_GYROSCOPE_X = Gx*Parameters.GLOBAL_TIME_PERIOD # Disengage for improved performance
    # State.DELTA_ORIENTATION_GYROSCOPE_Y = Gy*Parameters.GLOBAL_TIME_PERIOD # Disengage for improved performance
    State.DELTA_ORIENTATION_GYROSCOPE_Z = Gz*Parameters.GLOBAL_TIME_PERIOD
    
    return

def Update_Orientation():
    # Update_Accelerometer_Orientation() # Update the accelerometer orientation, disengage for improved performance
    Update_Magnetometer_Orientation() # Update the magnetometer orientation
    Read_Delta_Gyroscope_Orientation() # Update the change in gyroscope orientation
    
    # Use a High-pass/Low-pass complementary filter to combine the orientation data from the accelerometer, gyroscope and magnetometer to compute the sensor array's orientation
    # These orientation values compensate for noise, bias and drift
    # State.ORIENTATION_X = Parameters.HIGH_PASS_FILTER_MULTIPLIER_ALPHA*(State.ORIENTATION_X+State.DELTA_ORIENTATION_GYROSCOPE_X) + Parameters.LOW_PASS_FILTER_MULTIPLIER_ALPHA*(State.ORIENTATION_ACCELEROMETER_X) # Disengage for improved performance
    # State.ORIENTATION_Y = Parameters.HIGH_PASS_FILTER_MULTIPLIER_ALPHA*(State.ORIENTATION_Y+State.DELTA_ORIENTATION_GYROSCOPE_Y) + Parameters.LOW_PASS_FILTER_MULTIPLIER_ALPHA*(State.ORIENTATION_ACCELEROMETER_Y) # Disengage for improved performance
    State.ORIENTATION_Z = Parameters.HIGH_PASS_FILTER_MULTIPLIER_BETA*(State.ORIENTATION_Z+State.DELTA_ORIENTATION_GYROSCOPE_Z) + Parameters.LOW_PASS_FILTER_MULTIPLIER_BETA*(State.ORIENTATION_MAGNETOMETER_Z)
    return

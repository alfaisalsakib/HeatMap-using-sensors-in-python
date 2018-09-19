import Parameters
import HMC5883L
import MPU9250
import GY521
import Tools
import State

import math
import time

def Update_Reference_Orientation():
    print("Updating the Reference frame orientation. . .", end="")
    orientation_array = [0.0]*Parameters.REFERENCE_FRAME_ORIENTATION_SAMPLE_COUNT
    sentinel = True
    attempt_count = 0
    while sentinel:
        attempt_count += 1
        sentinel = False
        for iterator in range(Parameters.REFERENCE_FRAME_ORIENTATION_SAMPLE_COUNT):
            Tools.Update_Orientation()
            orientation_array[iterator] = State.ORIENTATION_Z
            time.sleep(0.001) # Limit the data acquisition rate to a maximum of 1kHz
        print(" Attempt "+str(attempt_count)+",", end="")
        for iterator in range(Parameters.REFERENCE_FRAME_ORIENTATION_SAMPLE_COUNT-1):
            if abs(orientation_array[iterator]-orientation_array[iterator+1]) > Parameters.REFERENCE_FRAME_ORIENTATION_TOLERANCE:
                sentinel = True
                break
    
    State.REFERENCE_ORIENTATION_Z = orientation_array[0]
    for iterator in range(Parameters.REFERENCE_FRAME_ORIENTATION_SAMPLE_COUNT-1):
        State.REFERENCE_ORIENTATION_Z += orientation_array[iterator+1]
        State.REFERENCE_ORIENTATION_Z /= 2.0
    
    print(" Success!")
    # print("Reference Orientation Z: " + str(State.REFERENCE_ORIENTATION_Z))
    return

# Calibrates the accelerometer by calculating the bias in its readouts that is caused by the gravitional acceleration and returns the calibration time
def Calibrate_Accelerometer_2_Data():
    start_time_overall = time.perf_counter() # Mark start time
    
    print("Calibrating the Bootstrap Accelerometer. . .", end="")
    avg_x, avg_y, avg_z = MPU9250.Probe_Accelerometer() # Load the initial set of values from the sensor
    
    end_time = time.perf_counter() + Parameters.MEAN_CALIBRATION_TIME # Run the calibration routine over the specified number of seconds
    start_time = time.perf_counter() # Mark the initial starting time
    while start_time<=end_time:
        time.sleep(Parameters.GLOBAL_TIME_PERIOD) # Limit the averaging frequency to a maximum of 1kHz because that's the configured update rate of the accelerometer
        inst_x, inst_y, inst_z = MPU9250.Probe_Accelerometer() # Load the instantaneous set of values from the sensor
        
        # Calculate the statistical mean
        avg_x += inst_x
        avg_x /= 2.0
        avg_y += inst_y
        avg_y /= 2.0
        avg_z += inst_z
        avg_z /= 2.0
        
        start_time = time.perf_counter() # Update the starting time
    
    State.GRAVITIONAL_ACCELERATION_2 = math.sqrt(avg_x*avg_x + avg_y*avg_y + avg_z*avg_z)
    
    print(" Success!")
    end_time_overall = time.perf_counter() # Mark end time
    return (end_time_overall - start_time_overall) # Return the time elapsed to calibrate the accelerometer

# Calibrates the accelerometer by calculating the bias in its readouts that is caused by the gravitional acceleration and returns the calibration time
def Calibrate_Accelerometer_Data():
    start_time_overall = time.perf_counter() # Mark start time
    
    print("Calibrating the Handheld Accelerometer. . .", end="")
    avg_x, avg_y, avg_z = GY521.Probe_Accelerometer() # Load the initial set of values from the sensor
    
    end_time = time.perf_counter() + Parameters.MEAN_CALIBRATION_TIME # Run the calibration routine over the specified number of seconds
    start_time = time.perf_counter() # Mark the initial starting time
    while start_time<=end_time:
        time.sleep(Parameters.GLOBAL_TIME_PERIOD) # Limit the averaging frequency to a maximum of 1kHz because that's the configured update rate of the accelerometer
        inst_x, inst_y, inst_z = GY521.Probe_Accelerometer() # Load the instantaneous set of values from the sensor
        
        # Calculate the statistical mean
        avg_x += inst_x
        avg_x /= 2.0
        avg_y += inst_y
        avg_y /= 2.0
        avg_z += inst_z
        avg_z /= 2.0
        
        start_time = time.perf_counter() # Update the starting time
    
    State.GRAVITIONAL_ACCELERATION = math.sqrt(avg_x*avg_x + avg_y*avg_y + avg_z*avg_z)
    
    print(" Success!")
    end_time_overall = time.perf_counter() # Mark end time
    return (end_time_overall - start_time_overall) # Return the time elapsed to calibrate the accelerometer

# Calibrates the gyroscope by calculating the bias in its readouts and returns the calibration time
def Calibrate_Raw_Gyroscope_Data():
    start_time_overall = time.perf_counter() # Mark start time
    
    print("Calibrating the Handheld Gyroscope. . .", end="")
    avg_x, avg_y, avg_z = GY521.Read_Raw_Gyroscope_Data() # Load the initial set of values from the sensor
    
    end_time = time.perf_counter() + Parameters.MEAN_CALIBRATION_TIME # Run the calibration routine over the specified number of seconds
    start_time = time.perf_counter() # Mark the initial starting time
    while start_time<=end_time:
        time.sleep(Parameters.GLOBAL_TIME_PERIOD) # Limit the averaging frequency to a maximum of 1kHz because that's the configured update rate of the accelerometer
        inst_x, inst_y, inst_z = GY521.Read_Raw_Gyroscope_Data() # Load the instantaneous set of values from the sensor
        
        # Calculate the statistical mean
        avg_x += inst_x
        avg_x /= 2.0
        avg_y += inst_y
        avg_y /= 2.0
        avg_z += inst_z
        avg_z /= 2.0
        
        start_time = time.perf_counter() # Update the starting time
    
    State.RAW_BIAS_GYROSCOPE_X = avg_x
    State.RAW_BIAS_GYROSCOPE_Y = avg_y
    State.RAW_BIAS_GYROSCOPE_Z = avg_z
    
    print(" Success!")
    end_time_overall = time.perf_counter() # Mark end time
    return (end_time_overall - start_time_overall) # Return the time elapsed to calibrate the gyroscope

# Calibrates the hard iron bias values for the magnetometer axes
def Calibrate_Raw_Magnetometer_Data():
    minX = 256000 # Arbitrarily large value
    maxX = -256000 # Arbitrarily small value
    minY = 256000 # Arbitrarily large value
    maxY = -256000 # Arbitrarily small value
    minZ = 256000 # Arbitrarily large value
    maxZ = -256000 # Arbitrarily small value
    
    count = 0
    while count<20000:
        Mx, My, Mz = HMC5883L.Read_Raw_Magnetometer_Data()
        
        if Mx<minX:
            minX=Mx
        elif Mx>maxX:
            maxX=Mx
        
        if My<minY:
            minY=My
        elif My>maxY:
            maxY=My
        
        if Mz<minZ:
            minZ=Mz
        elif Mz>maxZ:
            maxZ=Mz
        
        count+=1
    
    print("MAGNETOMETER CALIBRATION RESULTS\n--------------------------------")
    print("  Min(X) = "+str(minX))
    print("  Max(X) = "+str(maxX))
    print("  Min(Y) = "+str(minY))
    print("  Max(Y) = "+str(maxY))
    print("  Min(Z) = "+str(minZ))
    print("  Max(Z) = "+str(maxZ))
    print("\n  HARD IRON BIAS VALUES\n  ---------------------")
    print("    Bias(X) = "+str(-maxX -minX))
    print("    Bias(Y) = "+str(-maxY -minY))
    print("    Bias(Z) = "+str(-maxZ -minZ))
    
    return

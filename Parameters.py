MEAN_CALIBRATION_TIME = 5 # Time, in seconds, to run the statistical mean calibration routine for

GLOBAL_TIME_PERIOD = 0.01 # Determines the time period, in seconds, i.e. frequency of the HeatMap program. MINIMUM value is 0.001s i.e. 1kHz

# High-pass/Low-pass complementary filter multipliers; Set Alpha
# A higher value for the High-pass filter multiplier increases the readings' stability but at an increased lag
HIGH_PASS_FILTER_MULTIPLIER_ALPHA = 0.95 # Determines the fraction of signal to pass through during high pass filtering
LOW_PASS_FILTER_MULTIPLIER_ALPHA = 1 - HIGH_PASS_FILTER_MULTIPLIER_ALPHA # Calculated automatically, do not modify manually

# High-pass/Low-pass complementary filter multipliers; Set Beta
# A higher value for the High-pass filter multiplier increases the readings' stability but at an increased lag
HIGH_PASS_FILTER_MULTIPLIER_BETA = 0.97 # Determines the fraction of signal to pass through during high pass filtering
LOW_PASS_FILTER_MULTIPLIER_BETA = 1 - HIGH_PASS_FILTER_MULTIPLIER_BETA # Calculated automatically, do not modify manually

# Gain values for the individual accelerometer axes
ACCELEROMETER_X_GAIN = 1.0251 # Found experimentally, so the gravitional aceleration is as close to 9.80665 m/s^2 as possible
ACCELEROMETER_Y_GAIN = 1.0145 # Found experimentally, so the gravitional aceleration is as close to 9.80665 m/s^2 as possible
ACCELEROMETER_Z_GAIN = 0.9352 # Found experimentally, so the gravitional aceleration is as close to 9.80665 m/s^2 as possible

# Hard Iron Magnetometer axes bias compensations; found experimentally
BIAS_RAW_MAGNETOMETER_X = 0
BIAS_RAW_MAGNETOMETER_Y = 0
BIAS_RAW_MAGNETOMETER_Z = 0

MAGNETOMETER_ORIENTATION_OFFSET = 0.0 # Found experimentally

REFERENCE_FRAME_ORIENTATION_TOLERANCE = 1
REFERENCE_FRAME_ORIENTATION_SAMPLE_COUNT = 256

FOOTSTEP_ACCELERATION_THRESHOLD = 3.2
FOOTSTEP_TIME_LOCALITY_THRESHOLD = 0.8

FOOTSTEP_LENGTH = 1.267 # Nuren's average footstep length

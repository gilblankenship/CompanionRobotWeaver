
import time
import RPi.GPIO as GPIO

# Define the GPIO pins for the ping sensors and the driven wheels
PING_SENSOR_LEFT = 17
PING_SENSOR_RIGHT = 27
WHEEL_LEFT_FORWARD = 22
WHEEL_LEFT_BACKWARD = 23
WHEEL_RIGHT_FORWARD = 24
WHEEL_RIGHT_BACKWARD = 25

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PING_SENSOR_LEFT, GPIO.IN)
GPIO.setup(PING_SENSOR_RIGHT, GPIO.IN)
GPIO.setup(WHEEL_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(WHEEL_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(WHEEL_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(WHEEL_RIGHT_BACKWARD, GPIO.OUT)

# Define the constants for the robot's speed and turning radius
ROBOT_SPEED = 0.5
TURNING_RADIUS = 0.1

# Define the function to get the distance to an obstacle from a ping sensor
def get_distance_to_obstacle(ping_sensor):
  # Send a ping from the sensor
  GPIO.output(ping_sensor, GPIO.HIGH)
  time.sleep(0.00001)
  GPIO.output(ping_sensor, GPIO.LOW)

  # Get the time it takes for the echo to return
  start_time = time.time()
  while GPIO.input(ping_sensor) == GPIO.LOW:
    start_time = time.time()

  end_time = time.time()

  # Calculate the distance to the obstacle
  distance = (end_time - start_time) * 34300 / 2

  return distance

# Define the function to move the robot forward
def move_forward():
  GPIO.output(WHEEL_LEFT_FORWARD, GPIO.HIGH)
  GPIO.output(WHEEL_LEFT_BACKWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_FORWARD, GPIO.HIGH)
  GPIO.output(WHEEL_RIGHT_BACKWARD, GPIO.LOW)

# Define the function to move the robot backward
def move_backward():
  GPIO.output(WHEEL_LEFT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_LEFT_BACKWARD, GPIO.HIGH)
  GPIO.output(WHEEL_RIGHT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_BACKWARD, GPIO.HIGH)

# Define the function to turn the robot left
def turn_left():
  GPIO.output(WHEEL_LEFT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_LEFT_BACKWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_FORWARD, GPIO.HIGH)
  GPIO.output(WHEEL_RIGHT_BACKWARD, GPIO.LOW)

# Define the function to turn the robot right
def turn_right():
  GPIO.output(WHEEL_LEFT_FORWARD, GPIO.HIGH)
  GPIO.output(WHEEL_LEFT_BACKWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_BACKWARD, GPIO.LOW)

# Define the function to stop the robot
def stop():
  GPIO.output(WHEEL_LEFT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_LEFT_BACKWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_FORWARD, GPIO.LOW)
  GPIO.output(WHEEL_RIGHT_BACKWARD, GPIO.LOW)

# Define the main loop
while True:
  # Get the distance to the obstacles on the left and right sides of the robot
  distance_to_obstacle_left = get_distance_to_obstacle(PING_SENSOR_LEFT)
  distance_to_obstacle_right = get_distance_to_obstacle(PING_SENSOR_RIGHT)

  # If there is an obstacle on the left side of the robot, turn right
  if distance_to_obstacle_left < TURNING_RADIUS:
    turn_right()

  # If there is an obstacle on the right side of the robot, turn left
  elif distance_to_obstacle_right < TURNING_RADIUS:
    turn_left
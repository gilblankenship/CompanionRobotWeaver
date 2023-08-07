import cv2
import numpy as np
import time

# Define the camera resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Define the color of the tennis ball
BALL_COLOR = (0, 255, 255)

# Define the minimum and maximum area of the tennis ball
MIN_BALL_AREA = 100
MAX_BALL_AREA = 1000

# Initialize the ping sensors
ping_sensors = [
    PingSensor(17),
    PingSensor(27),
    PingSensor(22),
    PingSensor(10),
]

# Initialize the two driven wheels
left_wheel = Motor(13, 19)
right_wheel = Motor(26, 21)

# Define the speed of the two driven wheels
LEFT_WHEEL_SPEED = 100
RIGHT_WHEEL_SPEED = 100

# Create a function to find the tennis ball in the image
def find_ball(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the tennis ball color
    ball_mask = cv2.inRange(hsv_image, BALL_COLOR, BALL_COLOR)

    # Find the contours in the ball mask
    contours, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour in the ball mask
    largest_contour = max(contours, key=cv2.contourArea)

    # If the largest contour is too small, return None
    if cv2.contourArea(largest_contour) < MIN_BALL_AREA:
        return None

    # Calculate the center of the largest contour
    (x, y, w, h) = cv2.boundingRect(largest_contour)
    center = (x + w // 2, y + h // 2)

    # Return the center of the largest contour
    return center

# Create a function to control the robot
def control_robot(center):
    # If the tennis ball is not found, stop the robot
    if center is None:
        left_wheel.stop()
        right_wheel.stop()
        return

    # Calculate the distance to the tennis ball
    distance = get_distance_to_object(center)

    # If the tennis ball is too close, stop the robot
    if distance < 100:
        left_wheel.stop()
        right_wheel.stop()
        return

    # If the tennis ball is too far, drive towards it
    if distance > 200:
        left_wheel.set_speed(LEFT_WHEEL_SPEED)
        right_wheel.set_speed(RIGHT_WHEEL_SPEED)
        return

    # If the tennis ball is at the right distance, turn towards it
    if distance < 200 and distance > 100:
        if center[0] < CAMERA_WIDTH // 2:
            left_wheel.set_speed(LEFT_WHEEL_SPEED)
            right_wheel.set_speed(-RIGHT_WHEEL_SPEED)
        else:
            left_wheel.set_speed(-LEFT_WHEEL_SPEED)
            right_wheel.set_speed(RIGHT_WHEEL_SPEED)
        return

# Create a function to get the distance to an object
def get_distance_to_object(center):
    # Get the distance to the object from each ping sensor
    distances = [ping_sensor.get_distance() for ping_sensor in ping_sensors]

    # Calculate the average distance to the object
    average_distance = np.mean(distances)

    # Return the average distance to the object

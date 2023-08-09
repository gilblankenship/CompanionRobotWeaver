```python
import time
import numpy as np
import cv2
import pyrealsense2 as rs
import math
import serial

# initialize the camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# initialize the facial recognition model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# initialize the RTK GPS
gps = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# initialize the two driven wheels
left_wheel = 12
right_wheel = 13

# define the function to search for a known person
def search_for_person(known_person):
  # get the current frame from the camera
  frames = pipeline.wait_for_frames()
  depth_frame = frames.get_depth_frame()
  color_frame = frames.get_color_frame()

  # convert the depth frame to a numpy array
  depth_image = np.asarray(depth_frame.get_data())

  # convert the color frame to a numpy array
  color_image = np.asarray(color_frame.get_data())

  # find all faces in the color image
  faces = face_cascade.detectMultiScale(color_image, 1.3, 5)

  # loop over the faces
  for (x, y, w, h) in faces:
    # crop the face from the color image
    face_image = color_image[y:y+h, x:x+w]

    # resize the face image to the size of the facial recognition model
    face_image = cv2.resize(face_image, (160, 160))

    # predict the person's identity using the facial recognition model
    prediction = model.predict(face_image)

    # if the person is a known person, return their location
    if prediction[0] == known_person:
      return (x + w / 2, y + h / 2)

  # the person was not found
  return None

# define the function to drive the robot to a location
def drive_to_location(x, y):
  # calculate the distance and angle to the location
  distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
  angle = math.atan2(y - center_y, x - center_x)

  # set the speed of the two driven wheels
  left_speed = distance * math.cos(angle)
  right_speed = distance * math.sin(angle)

  # send the speed commands to the two driven wheels
  ser.write(str(left_speed) + ' ' + str(right_speed) + '\n')

# define the main loop
while True:
  # get the current location of the robot
  (center_x, center_y) = get_location()

  # search for the known person
  person_location = search_for_person(known_person)

  # if the person is found, drive to their location
  if person_location is not None:
    drive_to_location(person_location[0], person_location[1])

  # sleep for 100 milliseconds
  time.sleep(0.1)
```
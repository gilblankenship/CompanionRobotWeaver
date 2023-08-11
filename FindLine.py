import cv2
import numpy as np
import random

class Robot:
  """A class representing a robot."""

  def __init__(self, x, y, orientation):
    """Creates a new robot at the given position and orientation."""
    self.x = x
    self.y = y
    self.orientation = orientation

  def turn(self, direction):
    """Turns the robot in the given direction."""
    self.orientation += direction

  def move(self, distance):
    """Moves the robot forward by the given distance."""
    new_x = self.x + distance * np.cos(self.orientation)
    new_y = self.y + distance * np.sin(self.orientation)
    self.x = new_x
    self.y = new_y

def find_line(image):
  """Finds the line in the given image."""
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray_image, 50, 150)
  lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
  if lines is not None:
    return lines[0]
  print((lines[0]))
  return None

def follow_line(robot, line):
  """Makes the robot follow the given line."""
  start_point = line[0]
  end_point = line[0]
  direction = end_point - start_point
  if np.all(direction == 0):
    direction = [1, 0]
  direction = direction / np.linalg.norm(direction)
  robot.turn(direction)
  robot.move(0.1)
  print("Position: (%f, %f), orientation: %f" % (robot.x, robot.y, robot.orientation))
    
def generate_random_starting_point():
  x = random.random()
  y = random.random()
  theta = random.randint(0, 360)
  return x, y, theta

if __name__ == "__main__":
  image = cv2.imread("image.jpg")
  line = find_line(image)
  if line is not None:
    x, y, theta = generate_random_starting_point()
    robot = Robot(x,y,theta)
    print("Initial position: (%f, %f), orientation: %f" % (robot.x, robot.y, robot.orientation))
    follow_line(robot, line)
  else:
    print("No line found.")

import cv2
# Initialize the camera
cap = cv2.VideoCapture(0)
# Check if the camera is connected
if not cv2.VideoCapture(0).isOpened():
  print('The camera is not connected.')
  exit()

# Read a frame from the camera
ret, frame = cap.read()

# Check if there is a face in the frame
grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(grayscale_frame, 1.3, 5)
if len(faces) == 0:
  print('There is no face in the frame.')
  exit()

# Write the frame to a file
for (x, y, w, h) in faces:
  filename = 'faces/face_{}.jpg'.format(len(faces))
  cv2.imwrite(filename, frame[y:y+h, x:x+w])

# Release the camera
cap.release()

# Close all windows
cv2.destroyAllWindows()

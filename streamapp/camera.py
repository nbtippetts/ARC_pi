from imutils.video import VideoStream
from django.conf import settings
import threading
import argparse
import datetime
import imutils
import time
import cv2
import os


class VideoCamera(object):
	def __init__(self):
		print('Starting webcam video.')
		os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
		self.video = cv2.VideoCapture(0)
		self.stopped = False

	def get_frame(self):
		while not self.stopped:
			break
		else:
			self.stop()
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()

	def stop(self):
		self.stopped = True

# class VideoCamera(object):
# 	def __init__(self):
# 		print('Starting webcam video.')
# 		# os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"
# 		self.video = cv2.VideoCapture(0)
# 		(self.grabbed, self.image) = self.video.read()
# 		self.stopped = False

# 	def get_frame(self):
# 		while not self.stopped:
# 			if not self.grabbed:
# 				self.stop()
# 			else:
# 				time.sleep(0.5)
# 				(self.grabbed, self.image) = self.video.read()
# 				gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
# 				frame_flip = cv2.flip(self.image,1)
# 				self.ret, self.jpeg = cv2.imencode('.jpg', frame_flip)
# 				yield (b'--frame\r\n'
# 					b'Content-Type: image/jpeg\r\n\r\n' + self.jpeg.tobytes() + b'\r\n\r\n')

# 	def stop(self):
# 		self.stopped = True
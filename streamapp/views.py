from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera
from django.contrib.auth.decorators import login_required
import time

@login_required
def index(request):
	return render(request, 'video_view.html')


def gen(camera):
	while True:
		if camera.stopped:
			print('shutting down camera')
			break
		print('Camera is running')
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	try:
		return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')
	except Exception as e:
		print(e)
		pass
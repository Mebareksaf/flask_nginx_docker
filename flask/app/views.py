from app import app
import cv2 
import urllib.request
import numpy as np
from flask import Flask, render_template, Response


#we set our routes
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    #get url of esp cam
    url = "http://192.168.137.4/cam-hi.jpg" 
    while True:
        # get frams
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)            
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
        img = cv2.flip(img,-1)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


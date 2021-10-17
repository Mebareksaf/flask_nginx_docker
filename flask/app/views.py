from app import app
import cv2 
import urllib.request
import numpy as np
from flask import Flask, render_template, Response


@app.route('/')
def index():

    return render_template('index.html')

def gen():
    #get url of esp cam
    url = "http://X.X.X.X/cam-hi.jpg" 
    while True:
        # get frams
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)            
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


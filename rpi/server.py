#!/home/pi/gertduino/motor_test/pyenv/bin/python
###############################################################################################################                                                          
# Program Name: Browser_Client_Coder.html                                     
# ================================     
# This code is for controlling a robot by a web browser using web sockets                            
# http://www.dexterindustries.com/                                                                
# History
# ------------------------------------------------
# Author     Comments
# Joshwa     Initial Authoring
#                                                                  
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
###############################################################################################################

# CONNECTIONS-
#     Left Motor  - Port A
#     Right Motor - Port D
#
# PREREQUISITES
#    Tornado Web Server for Python
#
# TROUBLESHOOTING:
#    Don't use Ctrl+Z to stop the program, use Ctrl+c.
#    If you use Ctrl+Z, it will not close the socket and you won't be able to run the program the next time.
#    If you get the following error:
#        "socket.error: [Errno 98] Address already in use "
#    Run this on the terminal:
#        "sudo netstat -ap |grep :9093"
#    Note down the PID of the process running it
#    And kill that process using:
#        "kill pid"
#    If it does not work use:
#        "kill -9 pid"
#    If the error does not go away, try changin the port number '9093' both in the client and server code

#from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import time
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.gen
import tornado

import pymjpeg
import rc

#c=0
#Initialize TOrnado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class JpegCameraHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
    self.set_header('Connection', 'close')
    self.set_header('Content-Type', 'image/jpeg')
    self.set_header('Expires', 'Mon, 1 Jan 2000 00:00:00 GMT')
    self.set_header('Pragma', 'no-cache')
 
    img = open('/tmp/mjpeg.jpg', 'rb').read()
    self.set_header('Content-length', str(len(img)))
    self.write(str(img))

class MjpegCameraHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def get(self):
    ioloop = tornado.ioloop.IOLoop.current()

    self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
    self.set_header('Connection', 'close')
    self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--boundarydonotcross')
    self.set_header('Expires', 'Mon, 1 Jan 2000 00:00:00 GMT')
    self.set_header('Pragma', 'no-cache')
 
 
    self.served_image_timestamp = time.time()
    my_boundary = "--boundarydonotcross\n"
    while True:
      img = open('/tmp/mjpeg.jpg', 'rb').read()
      interval = 0.5
      if self.served_image_timestamp + interval > time.time():
        self.write(my_boundary)
        self.write("Content-type: image/jpeg\r\n")
        self.write("Content-length: %s\r\n\r\n" % len(img))
        self.write(str(img))
        self.served_image_timestamp = time.time()
        yield tornado.gen.Task(self.flush)
    else:
        yield tornado.gen.Task(ioloop.add_timeout, ioloop.time() + interval)

#Code for handling the data sent from the webpage
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'connection opened...'
    def on_message(self, message):
        print message
        remote.write(message)
    def on_close(self):
        print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/camera.jpg', JpegCameraHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Ready"
        while running:
#            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.2)              # sleep for 200 ms

if __name__ == "__main__":
    global remote
    remote = rc.RemoteControl()
#    BrickPiSetup()                          # setup the serial port for communication
#    BrickPi.MotorEnable[PORT_A] = 1         #Enable the Motor A
#    BrickPi.MotorEnable[PORT_D] = 1         #Enable the Motor D
#    BrickPiSetupSensors()                   #Send the properties of sensors to BrickPi
    running = True
#    thread1 = myThread(1, "Thread-1", 1)
#    thread1.setDaemon(True)
#    thread1.start()  
    application.listen(9093)              #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()
  


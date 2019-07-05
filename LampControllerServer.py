from flask import Flask
from flask import request
from BallufLamp import BallufLamp
from IOLinkHub import IOLinkHub
from Color import *
import argparse
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--platform", required=True,
	help="name of the IoT platform and version: tw1 OR ms1")
args = vars(ap.parse_args())

# display a friendly message to the user
print("Using platform and version: {}!".format(args["platform"]))

#Params: local and Hub IP
hub = IOLinkHub('192.168.33.250','192.168.33.249')
for PortNo in range(0, 8):   
    BallufLamp().AttachToHub(hub,PortNo)
    
#Set mode to segment mode
for PortNo in range(0, 8):
    hub.Lamps[PortNo].SetMode('Segment')

#Set to Green- 3 user spec-Green segment color
for PortNo in range(0, 8):
    hub.Lamps[PortNo].SetSegmentsToTestThingWorx()

for PortNo in range(0, 8):
    color1 = RGB_Color(255, 255, 255)
    hub.Lamps[PortNo].SetUserSpecifiedColor(color1)

#Start flask
app = Flask(__name__)


@app.route('/<lamp_id>/<color>')
def home(lamp_id, color):
    print(lamp_id, )
    red, green, blue = color.split('_')
    color1 = RGB_Color(int(red), int(green), int(blue))
    hub.Lamps[int(lamp_id)].SetUserSpecifiedColor(color1)
    return ''


if __name__ == '__main__':
    
    if args["platform"] == "tw1":
        app.run(host='0.0.0.0',port='32345')
    elif args["platform"] == "ms1":
        app.run(host='0.0.0.0',port='32348')
    else:
        print ("platform name not found")
    
    

from picamera import PiCamera
from time import sleep
import paho.mqtt.client as mqtt
from datetime import datetime
import configparser 
config = configparser.RawConfigParser()
config.read('cam.ini')

MQTT_IP=config.get('MQTT', 'mqtt.server.ip') #my ip
MQTT_PORT=config.get('MQTT', 'mqtt.server.port') #1883 by default

IM_PATH = '/home/pi/Im'
now = datetime.now() # current date and time
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")
day_path = '/'+month+day
IM_DAY_PATH = IM_PATH + day_path
IMG_PACK_SIZE = 4

# Create target directory & all intermediate directories if don't exists
if not os.path.exists(IM_DAY_PATH):
    os.makedirs(IM_DAY_PATH)
    print("Directory " , IM_DAY_PATH ,  " Created ")
else:
    new_name = IM_DAY_PATH+'_OLD_'+time
    os.rename(IM_DAY_PATH, new_name) 
    print("Directory " , IM_DAY_PATH ,  " already exists and rename to "+new_name)
    os.makedirs(IM_DAY_PATH)

#mqtt init
client = mqtt.Client()
client.connect(MQTT_IP,MQTT_PORT,60)
#camer init
camera = PiCamera()
#camera.resolution=(1920,1080)
camera.framerate = 15
camera.start_preview()
for i in range(IMG_PACK_SIZE):
    #camera.start_preview()
    sleep(6)
    camera.capture(IM_DAY_PATH+'/Image%s.jpg' % i)
    client.publish("topic/image",i)
    #camera.stop_preview()
    #sleep(55)
camera.stop_preview()
client.disconnect()
print('Finished')


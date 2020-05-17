import paho.mqtt.client as mqtt
import mysql.connector
from datetime import date, datetime, timedelta
import re
import configparser 
config = configparser.RawConfigParser()
config.read('cam.ini')

#image queue
cur_image = '0000000000';
next_image1 = '0000000000';
next_image2 = '0000000000';
acc_image = '0000000000';
def set_image(im_number):
  cur_image = next_image1
  next_image1 = next_image2
  next_image2 = im_number

def get_image:
  if next_image <= acc_image:
    acc_image == next_image2
  elif cur_iamge <= acc_image:
    acc_image = next_image
  else:
    acc_image = cur_image
  return acc_image
  

#msql init
MYSQL_USER = config.get('MYSQL', 'mysql.user')
MYSQL_PASSWORD = config.get('MYSQL', 'mysql.password')
MYSQL_HOST = config.get('MYSQL', 'mysql.host')
MYSQL_DATABASE = config.get('MYSQL', 'mysql.database')

MQTT_SERVER=config.get('MQTT', 'mqtt.server.ip')# my IP "192.168.0.112"
MQTT_PORT=config.get('MQTT', 'mqtt.server.port') #1883

CAM_MQTT_SERVER=config.get('MQTT', 'cam.mqtt.server.port') #cam server IP "192.168.0.109"
CAM_MQTT_PORT=config.get('MQTT', 'cam.mqtt.server.port') #1883

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                              host=MYSQL_HOST,
                              database=MYSQL_DATABASE)
cursor = cnx.cursor()
add_image = ("INSERT INTO image (im_number, im_datetime) VALUES (%s, %s)")

def get_image_db(im_number):
  data_image = (im_number, datetime.now())
  cursor.execute(add_image, data_image)
  id = cursor.lastrowid
  cnx.commit()
  set_image(id)

def  insert_object_db

#init mqtt topic/image
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/image")

def on_message(client, userdata, msg):
  im_number = msg.payload.decode()
  insert_im_db(im_number)
  print(cur_image)

client = mqtt.Client("ClientImage")
client.connect(CAM_MQTT_SERVER, CAM_MQTT_PORT,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()

#mqtt init topic/task
client_task = mqtt.Client("ClientTask")
client_task.connect(MQTT_SERVER,MQTT_PORT,60)

def send_task(ip,task)
  client_task.publish("topic/task",ip+':'+task)

#init mqtt topic/status
def on_connect_st(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/status")

def on_message_st(client, userdata, msg):
  msg = msg.payload.decode()
  #192.168.0.110:23
  ip = re.search('(\d+.\d+.\d+.\d+):\d+', msg).group(1)
  st_number = re.search('\d+.\d+.\d+.\d+:(\d+)', msg).group(1)
  prev_task = acc_number
  flag_send = False
  if st_number <= prev_task:
    task = get_image
    if task > prev_task:
      send_task(ip:task)
      flag_send = True
  if not flag_send:
    send_task(ip,0)
  print()
  
client_status = mqtt.Client("ClientStatus")
client_status.connect(MQTT_SERVER,MQTT_PORT,60)
client_status.on_connect = on_connect_st
client_status.on_message = on_message_st
client_status.loop_forever()

